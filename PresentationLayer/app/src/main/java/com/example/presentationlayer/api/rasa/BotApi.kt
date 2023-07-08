package com.example.presentationlayer.api.rasa


import com.example.presentationlayer.model.BotMessage
import com.example.presentationlayer.model.UserMessage
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface BotApi {
    @POST("webhook")
    fun messageBot(@Body userMessage: UserMessage): Call<List<BotMessage>>
}