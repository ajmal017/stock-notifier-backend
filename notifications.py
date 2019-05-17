import requests
import json

def main():
	endpoint = "https://fcm.googleapis.com/fcm/send"
	headers = {"Content-Type": "application/json",
	"Authorization": "key="}
	data = {"notification" : {
	 "body" : "This is a test",
	 "title": "Test"
	 }
	}
	r = requests.post(url = endpoint, data=json.dumps(data), headers=headers)


if __name__== "__main__":
  main()