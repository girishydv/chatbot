from wit import Wit

access_token = 'F46COF2YGJDQZLFIETD6JTJ3L6IJFGNW'
client = Wit(access_token=access_token)

def wit_resp(message_text):
    print('inside wit_reponse')
    resp=client.message(message_text)
    print('wit reponse::',resp)
    entity=None
    value=None

    try:
        entity= list(resp['entities'])[0]
        print('entity::',entity)
        value = resp['entities'][entity][0]['value']
        print('value::',value)
    except:
        pass
    return (entity,value)

print(wit_resp('I want sports news'))