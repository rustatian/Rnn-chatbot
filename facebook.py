from flask import Flask, request
import requests
from chatbot import chatbot
import better_exceptions

app = Flask(__name__)

ACCESS_TOKEN = "-"


class Chatbotmanager:
    bot = None
    def __init__(self):
        bot = chatbot.Chatbot()

    @app.route('/', methods=['GET'])
    def handle_verification(self):
        return request.args['hub.challenge']

    def reply(self, user_id, msg):
        data = {
            "recipient": {"id": user_id},
            "message": {"text": msg}
        }
        resp = requests.post("https://graph.facebook.com/v2.9/me/messages?access_token=" + ACCESS_TOKEN, json=data)
        print(resp.content)

    @app.route('/', methods=['POST'])
    def handle_incoming_messages(self):
        data = request.json
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        message = data['entry'][0]['messaging'][0]['message']['text']

        Chatbotmanager.bot = chatbot.Chatbot

        cb = chatbot.Chatbot
        prediction = cb.daemonPredict(self.bot, message)

        self.reply(sender, prediction)

        return "ok"


if __name__ == '__main__':
    app.run(debug=True)
