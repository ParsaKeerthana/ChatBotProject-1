from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = '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'

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    print("Received question:", question)  # Log the received question

    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Replace with the model you intend to use
            prompt=question,
            max_tokens=150  # Adjust as necessary
        )
        answer = response.choices[0].text.strip()
        print("OpenAI response:", answer)  # Log the OpenAI response
        return jsonify({'response': answer})
    except Exception as e:
        print("Error in OpenAI API call:", e)  # Log any errors
        return jsonify({'response': 'Error in processing the request'}), 500

if __name__ == '__main__':
    app.run(debug=True)
