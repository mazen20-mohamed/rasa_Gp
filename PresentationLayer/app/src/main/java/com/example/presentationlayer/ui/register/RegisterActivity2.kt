package com.example.presentationlayer.ui.register

import android.annotation.SuppressLint
import android.os.Bundle
import android.text.TextUtils
import android.util.Log
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.example.presentationlayer.R
import com.example.presentationlayer.api.spring.StartApi
import com.example.presentationlayer.model.User
import com.google.android.gms.tasks.OnCompleteListener
import com.google.android.material.textfield.TextInputEditText
import com.google.firebase.messaging.FirebaseMessaging
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


class RegisterActivity2 : AppCompatActivity() {

    @SuppressLint("MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register2)
        var btn = findViewById<Button>(R.id.btn_register2)

        var autoCompleteTextView = findViewById<AutoCompleteTextView>(R.id.activation_rate)
        var autoCompleteTextView2 = findViewById<AutoCompleteTextView>(R.id.gender)

        val subject = arrayOf("كسول", "نشط قليلا", "نشط بشكل معتدل","نشط جدا","نشط فوق المعتاد")
        val adapter= ArrayAdapter<String>(this, R.layout.dropdown, subject)
        autoCompleteTextView.setAdapter(adapter)


        val genderType = arrayOf("ذكر", "انثى")
        val adapter2= ArrayAdapter<String>(this, R.layout.dropdown, genderType)
        autoCompleteTextView2.setAdapter(adapter2)
        var gender:String = ""
        var activationRate:Double = 1.0

        autoCompleteTextView2.setOnClickListener {
//            autoCompleteTextView2.showDropdown(adapter2)
            gender = if(autoCompleteTextView2.text.toString() == "انثى"){
                "women"
            } else{
                "men"
            }
        }
        autoCompleteTextView.setOnClickListener {

//            autoCompleteTextView.showDropdown(adapter)
            activationRate = if(autoCompleteTextView.text.toString() == "كسول"){
                1.2
            } else if(autoCompleteTextView.text.toString() == "نشط قليلا") {
                1.4
            } else if(autoCompleteTextView.text.toString() == "نشط بشكل معتدل") {
                1.6
            } else if(autoCompleteTextView.text.toString() == "نشط جدا") {
                1.75
            } else{
                2.0
            }
        }

        btn.setOnClickListener{

            Log.d("###",gender)
            Log.d("###", activationRate.toString())
            if(gender=="" || activationRate==1.0){
                Toast.makeText(this,"النوع او معدل النشاط لم يتم اختياره",Toast.LENGTH_SHORT).show()
            }
            else{
                register(gender,activationRate)
            }

        }
        var image = findViewById<ImageView>(R.id.back_to_last)
        image.setOnClickListener{
            finish()
        }
    }
    fun register(gender:String , activationRate:Double){
        val instance: StartApi = StartApi()
        val bundle = intent.extras

        var name = bundle?.getString("name")
        var email = bundle?.getString("email")
        var password = bundle?.getString("password")
        var age  = findViewById<TextInputEditText>(R.id.age)
        var height  = findViewById<TextInputEditText>(R.id.height)
        var weight  = findViewById<TextInputEditText>(R.id.weight)
        FirebaseMessaging.getInstance().token.addOnCompleteListener(OnCompleteListener { task ->
            if (!task.isSuccessful) {
                return@OnCompleteListener
            }
            val token = task.result
            var user: User = User(name.toString(),email.toString(),password.toString(),weight.text.toString().toDouble(),height.text.toString().toInt(),age.text.toString().toInt(),activationRate,gender,token)
            if(age!=null && height!=null && weight!=null){
                instance.getInstance().register(user).
                enqueue(object: Callback<ResponseBody> {
                    override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                        if(response.isSuccessful){
                            Toast.makeText(this@RegisterActivity2,"تم انشاء حسابك بنجاح",Toast.LENGTH_LONG).show()
                            finish()
                        } else{
                            Toast.makeText(this@RegisterActivity2,"البريد الالكتروني تم استخدامه مسبقا",Toast.LENGTH_SHORT).show()
                        }
                    }
                    override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                        Log.d("#", t.message.toString())
                        Toast.makeText(this@RegisterActivity2,"هناك مشكلة في الاتصال",Toast.LENGTH_SHORT).show()
                    }
                }
                )
            }
            else{
                Toast.makeText(this,"العمر او الطول او الوزن لم يتم ادخاله",Toast.LENGTH_LONG).show()
            }
        })

    }
}
