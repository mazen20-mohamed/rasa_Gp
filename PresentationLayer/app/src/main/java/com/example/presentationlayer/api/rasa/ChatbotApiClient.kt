package com.example.presentationlayer.api.rasa

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.example.presentationlayer.model.BotMessage
import com.example.presentationlayer.model.Constants
import com.example.presentationlayer.model.Message
import com.example.presentationlayer.model.UserMessage
import retrofit2.Call
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.lang.Exception
import java.util.concurrent.Executors
import java.util.concurrent.Future
import java.util.concurrent.ScheduledExecutorService
import java.util.concurrent.TimeUnit
object ServiceGenerator {

    private val retrofitBuilder: Retrofit.Builder = Retrofit.Builder()
        .baseUrl(Constants.BASE_URL)
        .addConverterFactory(GsonConverterFactory.create())

    val CHAT_BOT_API: BotApi by lazy {
        retrofitBuilder.build()
            .create(BotApi::class.java)
    }

}
object AppExecutors {

    private val mNetworkIO: ScheduledExecutorService = Executors.newScheduledThreadPool(3)

    fun networkIO(): ScheduledExecutorService = mNetworkIO
}
object ChatBotApiClient {

    private val mBotResponse: MutableLiveData<List<BotMessage>> = MutableLiveData()
    private val mConversation: MutableLiveData<MutableList<Message>> = MutableLiveData()
    private var mBotQueryRunnable: BotQueryRunnable?= null


    fun getBotMessages(): LiveData<List<BotMessage>>  = mBotResponse

    fun getConversation(): LiveData<MutableList<Message>> = mConversation

    fun addUserMessageInConversation(userMessage: UserMessage) {
        var oldConversation: MutableList<Message>? = mConversation.value

        if(oldConversation==null) {
            var newConversation: MutableList<Message> = mutableListOf()
            newConversation.add(Message(message = userMessage.message, sender = Constants.USER))
            newConversation.add(Message(message = null, sender= Constants.LOADING))
            mConversation.postValue(newConversation)
        } else {
            oldConversation.add(Message(message = userMessage.message, sender = Constants.USER))
            oldConversation.add(Message(message = null, sender= Constants.LOADING))
            mConversation.postValue(oldConversation)
        }
    }

    private fun addBotMessageInConversation(botMessage: Message) {
        var oldConversation: MutableList<Message>? = mConversation.value

        if(oldConversation==null) {
            var newConversation: MutableList<Message> = mutableListOf()
            newConversation.add(botMessage)
            mConversation.postValue(newConversation)
        } else {
            if(oldConversation[oldConversation.size-1].sender== Constants.LOADING)
                oldConversation.removeAt(oldConversation.size-1)

            oldConversation.add(botMessage)
            mConversation.postValue(oldConversation)
        }
    }

    private fun isBotLoading(): Boolean{

        val currentConversation = mConversation.value ?: return false

        return (currentConversation.isNotEmpty() && currentConversation[currentConversation.size-1].sender== Constants.LOADING)
    }

    fun queryBot(sender: Int, message: String) {

        if(mBotQueryRunnable!=null) mBotQueryRunnable = null

        mBotQueryRunnable = BotQueryRunnable(sender, message)

        val handler: Future<*> = AppExecutors.networkIO().submit(mBotQueryRunnable)

        AppExecutors.networkIO().schedule(Runnable {

            // stop request - timeout occurred
            handler.cancel(true)


        }, Constants.NETWORK_TIMEOUT, TimeUnit.MILLISECONDS)

    }

    private class BotQueryRunnable(
        private var sender: Int,
        private var message: String,
        var cancelRequest: Boolean = false
    ): Runnable {


        override fun run() {

            try {

                val response:Response<List<BotMessage>> = getMessageBot(sender, message).execute()
                if(cancelRequest) return
                if(response.code()==200) {
                    val botResponseList: List<BotMessage> = (response.body() as List<BotMessage>)
                    botResponseList.let {
                        mBotResponse.postValue(botResponseList)

                        var prevConversations: List<Message>? = mConversation.value

                        var botMessages: MutableList<Message> = mutableListOf()

                        for(response in botResponseList) {
                            botMessages.add(
                                Message(
                                    message = response.response,
                                    sender = Constants.BOT,
                                    imageUrl = response.imageUrl
                                ))
                        }

                        if(prevConversations==null) {
                            mConversation.postValue(botMessages)

                        } else {

                            var oldConversation: MutableList<Message>? = mConversation.value
                            oldConversation?.let { list ->

                                // hide loading first
                                if(list[list.size-1].sender== Constants.LOADING) list.removeAt(list.size-1)

                                list.addAll(botMessages)
                                mConversation.postValue(list)
                            }
                        }
                    }

                } else {
                    addBotMessageInConversation(
                        Message(
                            message = "خطأ في الرد الرجاء ارسل رسالتك مرة اخرى",
                            sender = Constants.BOT
                        )
                    )
                }


            } catch (e: Exception) {
                e.printStackTrace()
                addBotMessageInConversation(
                    Message(
                        message = "غير متوفر حاليا انا اسف",
                        sender = Constants.BOT
                    )
                )
            }

        }
        private fun getMessageBot(sender: Int, message: String): Call<List<BotMessage>> = ServiceGenerator.CHAT_BOT_API.messageBot(
            userMessage = UserMessage(
                sender = sender,
                message= message
            )
        )
        // cancel bot request - may be on back press
        fun cancelRequest() {
            cancelRequest = true
        }
    }
}
