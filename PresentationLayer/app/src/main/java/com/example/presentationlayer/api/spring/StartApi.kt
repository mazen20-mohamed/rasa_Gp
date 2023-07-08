package com.example.presentationlayer.api.spring

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class StartApi {

    private val retrofit: ApiService = Retrofit.Builder()
    .baseUrl("https://f12d-154-179-50-61.eu.ngrok.io/demo/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()
    .create(ApiService::class.java)

    fun getInstance(): ApiService {
        return retrofit
    }
}
