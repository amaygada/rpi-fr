import requests
import os
import time

api = "https://241d-2405-201-17-f0cc-b498-3c83-3820-1a9c.ngrok.io/api/"

name = input("Enter your name: ")
email = input("Enter your email: ")

path = "/home/pi/facerecog/"+name+"/"

o = {}
for i in os.listdir(path):
	o[str(i)] = open(path+i, 'rb')

data = {"name": name, "email": email+"t"}

#try:
#	response = requests.post(api, data=data, files=o, timeout=10)
#except requests.exceptions.Timeout as err:
#	print(err)

t = time.time()
response = requests.post(api, data=data, files=o)

print(time.time() - t)

print(response)
print(response.text)
