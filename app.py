from flask import Flask, render_template, request, jsonify

from chatbot1 import ChatBot, extractSymptoms

bot=ChatBot()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process', methods=['POST'])
def process():
    user_message = request.form['user_input']
    bot_response = bot.sendMessage(user_message)
    # Replace the next line with your chatbot logic
    chatbot_response = bot_response
    return jsonify({'response': chatbot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=18100)
