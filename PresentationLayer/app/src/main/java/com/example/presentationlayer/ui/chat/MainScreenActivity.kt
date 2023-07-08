package com.example.presentationlayer.ui.chat


import android.content.Context
import android.graphics.drawable.Drawable
import android.os.Bundle

import android.view.View
import android.view.inputmethod.InputMethodManager
import android.widget.EditText
import android.widget.Toast
import android.widget.Toolbar
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.get
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.presentationlayer.R
import com.example.presentationlayer.viewModel.BotAdapter
import com.example.presentationlayer.viewModel.ChatBotViewModel
import com.google.android.material.appbar.MaterialToolbar
import com.google.android.material.floatingactionbutton.FloatingActionButton


class MainScreenActivity : AppCompatActivity(), View.OnClickListener {
    private lateinit var mMessageET: EditText
    private lateinit var mSendBtn: FloatingActionButton
    private lateinit var mChatRecyclerView: RecyclerView

    private lateinit var mChatBotViewModel: ChatBotViewModel
    private lateinit var mChatBotRecyclerAdapter: BotAdapter
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main_screen)
        mChatBotViewModel = ViewModelProvider(this)[ChatBotViewModel::class.java]

        mMessageET = findViewById(R.id.message_et)
        mSendBtn = findViewById(R.id.msg_btn)
        mChatRecyclerView = findViewById(R.id.recyclerView)

        initRecyclerView()
        subscribeObservers()

        mSendBtn.setOnClickListener(this)

        val topAppBar = findViewById<MaterialToolbar>(R.id.topApp)
        topAppBar.inflateMenu(R.menu.menu)

        topAppBar.setNavigationOnClickListener { finish() }
        topAppBar.setOnMenuItemClickListener {
            when(it.itemId){
                R.id.bot->click()
            }
            true
        }
    }
    private fun click(){
        val topAppBar = findViewById<MaterialToolbar>(R.id.topApp)
        topAppBar.get(R.id.bot).setBackgroundResource(R.drawable.lightbulb2)
        mChatRecyclerView.setBackgroundResource(R.drawable.lightbulb2)
    }
    private fun subscribeObservers() {  

        mChatBotViewModel.getBotMessages().observe(this, Observer {

        })

        mChatBotViewModel.getConversation().observe(this, Observer { conversation ->
            mChatBotRecyclerAdapter.setConversation(conversation)
            mChatRecyclerView.scrollToPosition(conversation.size-1)
        })
    }


    private fun initRecyclerView() {
        mChatBotRecyclerAdapter = BotAdapter()
        mChatRecyclerView.layoutManager = LinearLayoutManager(this)
        (mChatRecyclerView.layoutManager as LinearLayoutManager).stackFromEnd = true
        mChatRecyclerView.adapter = mChatBotRecyclerAdapter
    }

    override fun onClick(view: View?) {
        view?.let {
            when(view.id) {

                R.id.msg_btn -> {
                    val message = mMessageET.text.trim().toString()
                    if(!isMessageValid(message)) {
                        showToast("الرسالة فارغة")
                        return
                    }

                    mChatBotViewModel.addUserMessageInConversation(message)
                    mMessageET.text.clear()
                    hideKeyboard()
                    mMessageET.clearFocus()

                    // send user message to chat bot
                    mChatBotViewModel.queryBot(message)
                }
            }
        }
    }

    private fun hideKeyboard() {
        this.currentFocus?.let { view ->
            val imm = getSystemService(Context.INPUT_METHOD_SERVICE) as? InputMethodManager
            imm?.hideSoftInputFromWindow(view.windowToken, 0)
        }
    }

    private fun isMessageValid(message: String?): Boolean {
        return !(message==null || message.trim().isEmpty())
    }

    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }

}

