package com.stfalcon.chatkit.sample.features.demo.custom.media;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.util.ArrayMap;
import android.widget.Toast;

import androidx.annotation.RequiresApi;

import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.JsonRequest;
import com.android.volley.toolbox.Volley;
import com.stfalcon.chatkit.commons.models.IMessage;
import com.stfalcon.chatkit.commons.models.IUser;
import com.stfalcon.chatkit.messages.MessageHolders;
import com.stfalcon.chatkit.messages.MessageInput;
import com.stfalcon.chatkit.messages.MessagesList;
import com.stfalcon.chatkit.messages.MessagesListAdapter;
import com.stfalcon.chatkit.sample.R;
import com.stfalcon.chatkit.sample.common.data.fixtures.MessagesFixtures;
import com.stfalcon.chatkit.sample.common.data.model.Message;
import com.stfalcon.chatkit.sample.common.data.model.User;
import com.stfalcon.chatkit.sample.features.demo.DemoMessagesActivity;
import com.stfalcon.chatkit.sample.features.demo.custom.media.holders.IncomingVoiceMessageViewHolder;
import com.stfalcon.chatkit.sample.features.demo.custom.media.holders.OutcomingVoiceMessageViewHolder;

import org.json.JSONException;
import org.json.JSONObject;
import java.util.Map;

public class CustomMediaMessagesActivity extends DemoMessagesActivity
        implements MessageInput.InputListener,
        MessageInput.AttachmentsListener,
        MessageHolders.ContentChecker<Message>,
        DialogInterface.OnClickListener {

    private final String URL = "https://chatbot-prova.herokuapp.com/api/chatterbot/";

    private static final byte CONTENT_TYPE_VOICE = 1;

    public static void open(Context context) {
        context.startActivity(new Intent(context, CustomMediaMessagesActivity.class));
    }

    private final Response.Listener<JSONObject> successListener = response -> {
        try {
            String reply = response.getString("text");
            Message message = new Message("prova",new User("chatbot","chatbot",null,true),reply);


            messagesAdapter.addToStart(message,true);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    };

    private final Response.ErrorListener errorListener = error -> Toast.makeText(getApplicationContext(),error.toString(),Toast.LENGTH_SHORT).show();

    private MessageInput.InputListener listener = new MessageInput.InputListener() {
        @RequiresApi(api = Build.VERSION_CODES.KITKAT)
        @Override
        public boolean onSubmit(CharSequence input) {
            RequestQueue requestQueue = Volley.newRequestQueue(getApplicationContext());
            Map<String,String> text = new ArrayMap<>();
            text.put("text",input.toString());

            JSONObject request = new JSONObject(text);

            JsonObjectRequest objectRequest = new JsonObjectRequest(
                    Request.Method.POST,
                    URL,
                    request,
                    successListener,
                    errorListener
            );

            requestQueue.add(objectRequest);
            Message message = new Message("prova",new User("ale","ale",null,true),input.toString());
            messagesAdapter.addToStart(message,true);
            return true;
        }
    };

    private MessagesList messagesList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_custom_media_messages);

        this.messagesList = findViewById(R.id.messagesList);
        initAdapter();

        MessageInput input = findViewById(R.id.input);
        input.setInputListener(listener);
        input.setAttachmentsListener(this);
    }

    @Override
    public boolean onSubmit(CharSequence input) {
        super.messagesAdapter.addToStart(
                MessagesFixtures.getTextMessage(input.toString()), true);
        return true;
    }

    @Override
    public void onAddAttachments() {
        new AlertDialog.Builder(this)
                .setItems(R.array.view_types_dialog, this)
                .show();
    }

    @Override
    public boolean hasContentFor(Message message, byte type) {
        if (type == CONTENT_TYPE_VOICE) {
            return message.getVoice() != null
                    && message.getVoice().getUrl() != null
                    && !message.getVoice().getUrl().isEmpty();
        }
        return false;
    }

    @Override
    public void onClick(DialogInterface dialogInterface, int i) {
        switch (i) {
            case 0:
                messagesAdapter.addToStart(MessagesFixtures.getImageMessage(), true);
                break;
            case 1:
                messagesAdapter.addToStart(MessagesFixtures.getVoiceMessage(), true);
                break;
        }
    }

    private void initAdapter() {
        MessageHolders holders = new MessageHolders()
                .registerContentType(
                        CONTENT_TYPE_VOICE,
                        IncomingVoiceMessageViewHolder.class,
                        R.layout.item_custom_incoming_voice_message,
                        OutcomingVoiceMessageViewHolder.class,
                        R.layout.item_custom_outcoming_voice_message,
                        this);


        super.messagesAdapter = new MessagesListAdapter<>("ale", holders, super.imageLoader);
        super.messagesAdapter.enableSelectionMode(this);
        super.messagesAdapter.setLoadMoreListener(null);
        this.messagesList.setAdapter(super.messagesAdapter);
    }
}
