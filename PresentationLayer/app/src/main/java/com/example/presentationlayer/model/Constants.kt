package com.example.presentationlayer.model

class Constants {

    companion object {
        val NGROCK_URL = "https://7dee-154-179-50-61.eu.ngrok.io"
        val BASE_URL = "$NGROCK_URL/webhooks/rest/"
        val NETWORK_TIMEOUT = 5000L
        val MESSAGE_TEXT_NULL = "NA"

        var USER = 0
        val BOT = 1
        val LOADING = 2
    }
}