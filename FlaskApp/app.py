import os
import openai
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Setting the API key
openai.api_key = "INSERT_KEY"

# Initial system and assistant messages
messages = [
    {"role": "system", "content": "You are an expert travel agent who can assist any user with travel, itinerary, planning queries. Only answer questions if they are related to travel. Otherwise respond that you cannot answer outside travel domain questions."},
    {"role": "assistant", "content": "How can I help you with your travel related queries?"}
]

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')

    # Append the user's question to the messages
    messages.append({"role": "user", "content": user_question})

    # Get the assistant's response
    response = get_assistant_response(messages)

    # Append the assistant's response to the messages
    messages.append({"role": "assistant", "content": response})

    # Limit the history size to avoid overly long conversations
    messages = messages[-10:]  # Keep only the last 10 messages

    return jsonify({'response': response})

def get_assistant_response(messages):
    r = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages],
    )
    response = r.choices[0].message.content
    return response

if __name__ == '__main__':
    app.run(debug=True)
