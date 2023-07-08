package com.example.presentationlayer.model

data class Message(
    var message: String?= null,
    var sender: Int,
    var imageUrl: String?=null
)