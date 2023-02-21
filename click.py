import base64
import json
import requests
import subprocess
import os
import time

name = input("Enter your name: ")

# raspistill -n -t 1000 -w 768 -h 768 -a 1036 -ae +25+25 -o test.jpg

cmd = "raspistill"
path = "/home/pi/facerecog/" + str(name) + "/"


try:
	os.mkdir(path)
except:
	pass

print("waiting for 5 seconds before clicking pictures")
print("")

time.sleep(5)

for i  in range(10):
	temp = subprocess.Popen([cmd, "-w", "500", "-h", "500", "-o",  path+str(i)+".jpg"], stdout=subprocess.PIPE)
	temp.communicate()
	time.sleep(0.5)
	print(path+str(i)+".jpg")

print("pictures have been stored successfully")
