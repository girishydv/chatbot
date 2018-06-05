from wit import Wit
import json

access_token = 'F46COF2YGJDQZLFIETD6JTJ3L6IJFGNW'
client = Wit(access_token=access_token)

def wit_resp(message_text):
    resp=client.message(message_text)
    print('wit reponse::',resp)
    entities=None
    intentdict = {}

    try:
        entities= list(resp['entities'])
        print('entities::',entities)
        for entity in entities:
            intentdict.update({entity:[data['value'] for data in resp['entities'][entity]]})
            print('value::',intentdict)
    except:
        pass
    return (intentdict)

print(wit_resp('I want sports news'))