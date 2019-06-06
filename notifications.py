import requests
import json

def sendNotification(tokens, title, body, key):
        for token in tokens:
                print(type(token))
                print(type(key))
                print(type(title))
                print(type(body))
                endpoint = "https://fcm.googleapis.com/fcm/send"
                headers = {"Content-Type": "application/json",
                           "Authorization": key}
                data = {"notification" : {
                        "body" : body,
                        "title": title,
		        "sound": "default"
                },
                        "to": token
                }
                r = requests.post(url = endpoint, data=json.dumps(data), headers=headers)


#if __name__== "__main__":
#  main()
