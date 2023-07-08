package com.example.presentationlayer.ui.login

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import com.example.presentationlayer.R
import com.example.presentationlayer.api.spring.StartApi
import com.example.presentationlayer.ui.chat.MainScreenActivity
import com.example.presentationlayer.ui.register.RegisterActivity
import com.google.android.material.textfield.TextInputEditText
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
var userId:Int = 1
class LoginActivity : AppCompatActivity() {


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        var btn = findViewById<Button>(R.id.btn_login)
        btn.setOnClickListener{
            login()
        }

        var text = findViewById<TextView>(R.id.register_text)
        text.setOnClickListener{
            val intent = Intent(this@LoginActivity, RegisterActivity::class.java)
            startActivity(intent)
        }
    }
    fun login(){
        val instance: StartApi = StartApi()
        var email = findViewById<TextInputEditText>(R.id.emailInput)
        var password = findViewById<TextInputEditText>(R.id.passwordInput)
        instance.getInstance().login(email.text.toString(),password.text.toString())?.enqueue(
            object:Callback<Long?>{
                override fun onResponse(call: Call<Long?>, response: Response<Long?>) {
                    if(response.isSuccessful){
                        val nullable:Int? = response.body()?.toInt()
                        if(nullable!=null){
                            userId = nullable
                        }

                        val intent = Intent(this@LoginActivity, MainScreenActivity::class.java)
                        startActivity(intent)

                    } else{
                        Toast.makeText(this@LoginActivity,"البريد الالكتروني او كلمة السر غير صحيحة",Toast.LENGTH_SHORT).show()
                    }
                }

                override fun onFailure(call: Call<Long?>, t: Throwable) {
                    Toast.makeText(this@LoginActivity,"الاتصال بطئ",Toast.LENGTH_SHORT).show()
                }
            }
        )
    }
}
