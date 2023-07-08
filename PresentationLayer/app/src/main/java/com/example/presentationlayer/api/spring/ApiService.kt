package com.example.presentationlayer.api.spring

import com.example.presentationlayer.model.User
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

interface ApiService {
    @GET("login")
    fun login(@Query("email")email:String,@Query("password")password:String): Call<Long?>?

    @POST("register")
    fun register(@Body user: User): Call<ResponseBody>

}
