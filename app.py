from flask import Flask, request
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAAJG7m4urZB8BO7CYCbVBfYw5O7LshzZAZBuhi79UIZAZAlIlDywdY67NKT7H0d4eIM19iZAJmgBZAjIRNqo20zgFwIPpjZBBEqaOAeIRyUTosvqgZC4BtoHW4COBvQkZAKZA5MZBTQaTd6BUK1Vd2PCsYEgQW7AmKUeivvlb4ga348H07h43qHWWJlSFJwRlwlPjb3ZB'
VERIFY_TOKEN = 'test1313'

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args["hub.challenge"], 200
        return "Verification token mismatch", 403
    return "Hello world", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message'].get('text')
                    if message_text:
                        send_message(sender_id, "You sent the message: " + message_text)
    return "ok", 200

def send_message(recipient_id, message_text):
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }
    response = requests.post("https://graph.facebook.com/v11.0/me/messages", params=params, headers=headers, json=data)
    if response.status_code != 200:
        print('Failed to send message:', response.status_code, response.text)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
