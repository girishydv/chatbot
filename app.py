import os, sys
from flask import Flask, request
from utils import wit_resp
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
                    print('messaging_text::',messaging_text)
                    response=None
                    intentdict=wit_resp(messaging_text)
                    print('intentdict::',intentdict)
                    #for entity in intentdict:
                    if ('agenda_enter' in intentdict) & ('location' in intentdict) & ('datetime' in intentdict):
                        agenda = " ".join(str(x) for x in intentdict['agenda_entry'])
                        response = "OK, I will {0} for you {1} {2}".format(str(agenda), intentdict['location'][0],
                                                                           intentdict['datetime'][0])
                    elif 'location' in intentdict:
                        response = 'OK, you live in {0}. That\'s a fantastic place. I will send you top headlines from {0}'.format(str(intentdict['location'][0]))
                    if  'datetime' in intentdict:
                        response = 'what do you want me to do with this date'
                    if response==None:
                        response='Sorry I din\'t get you.'

                    bot.send_text_message(sender_id, response)
    return "OK", 200

def log(message):
    print(message)
    sys.stdout.flush()
    
if __name__ == "__main__":
    app.run(debug=True, port=80)
