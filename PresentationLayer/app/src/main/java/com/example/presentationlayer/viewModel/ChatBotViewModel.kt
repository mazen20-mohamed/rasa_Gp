package com.example.presentationlayer.viewModel

import androidx.lifecycle.LiveData
import androidx.lifecycle.ViewModel
import com.example.presentationlayer.model.Constants
import com.example.presentationlayer.model.BotMessage
import com.example.presentationlayer.model.Message
import com.example.presentationlayer.model.UserMessage
import com.example.presentationlayer.repo.ChatBotRepository

class ChatBotViewModel: ViewModel() {


    private val mChatBotRepository: ChatBotRepository = ChatBotRepository

    fun getBotMessages(): LiveData<List<BotMessage>> = ChatBotRepository.getBotMessages()

    fun getConversation(): LiveData<MutableList<Message>> = ChatBotRepository.getConversation()

    fun addUserMessageInConversation(message: String) {
        ChatBotRepository.addUserMessageInConversation(
            UserMessage(
                message = message,
                sender = Constants.USER
            )
        )
    }

    fun queryBot(message: String) {
        ChatBotRepository.queryBot(message)
    }

}