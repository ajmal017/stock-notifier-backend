import requests
import json

def sendNotification(tokens, title, body):
	for token in tokens:
		endpoint = "https://fcm.googleapis.com/fcm/send"
		headers = {"Content-Type": "application/json",
		"Authorization": "key="} #Add firebase authentication key 
		data = {"notification" : {
		 "body" : body,
		 "title": title
		 },
		 "to": token
		}
		r = requests.post(url = endpoint, data=json.dumps(data), headers=headers)


#if __name__== "__main__":
#  main()