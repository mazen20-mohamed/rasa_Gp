package com.example.presentationlayer.model
import com.example.presentationlayer.ui.login.userId


data class UserMessage(
    var sender: Int = userId,
    var message: String?= null
)
