import requests
import json

def sendNotification(tokens, title, body):
	for token in tokens:
		endpoint = "https://fcm.googleapis.com/fcm/send"
		headers = {"Content-Type": "application/json",
		"Authorization": "key=AAAAa84aHb0:APA91bEfZEDoHjHTjyCkBG_DVS_UKHYQ3mI_oi0KSpdQh2V_kgOndy1qkuAG86ijPFXQxMid_aaEgInACrQngL9gjMHSfFkAoBVbNb61KirJ_PiJcLQtVVdR2JJI2pF_2lhwDgANvFWi"} #Add firebase authentication key 
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