import os
import uuid

import vertexai

from flask import Flask, request, jsonify, make_response
from vertexai.preview.language_models import ChatModel

PROJECT_ID = os.environ.get("PROJECT_ID", "your-project-here")
LOCATION = os.environ.get("LOCATION", "us-central1")
vertexai.init(project=PROJECT_ID, location=LOCATION)
chat_model = ChatModel.from_pretrained("chat-bison@001")
parameters = {"temperature": 0.2, "max_output_tokens": 256, "top_p": 0.8, "top_k": 40}
chat_sessions = {}

app = Flask(__name__)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    session_id = request.cookies.get('session_id')
    if session_id is None or session_id not in chat_sessions:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = chat_model.start_chat(
            examples=[]
        )
    chat = chat_sessions[session_id]

    user_input = request.get_json()['input']
    response = chat.send_message(user_input, **parameters)
    chat_sessions[session_id] = chat

    response = make_response(jsonify({'response': response.text}))
    response.set_cookie('session_id', session_id)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')