import os, sys
from flask import Flask, request
from pymessenger import Bot


PAGE_ACCESS_TOKEN='EAAL5xxj8c7sBABSAp7zl67xGa7GRbB6HXqJDj6BZAI5k033hWVNOS1aIZBO7Lzv2Yb5nUozypLQAjWREa90D9QfQZBZAgOEE39VaLoiZANnieFZCkwxxPiMS5hLe9o9E2JeeY21Drzw0e9pSan2JnB92wZCpd7OHXi0zCeslcQxSQZDZD'
bot = Bot(PAGE_ACCESS_TOKEN)
app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # webhook  verification
    if (request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge")):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    # Echo
                    response = messaging_text
                    bot.send_text_message(sender_id, response)
    return "OK", 200

def log(message):
    print(message)
    sys.stdout.flush()
    
if __name__ == "__main__":
    app.run(debug=True, port=90)
