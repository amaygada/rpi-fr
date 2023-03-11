import requests
import time
import subprocess
import RPi.GPIO as GPIO
import os

api = "https://0467-2405-201-17-f0cc-149e-7d9d-191f-8435.ngrok.io/api/"
cmd = "raspistill"
thresh = 6

try :

	GPIO.setmode(GPIO.BOARD)
	resistor_pin=7

	print("INIT")

	while True:
		GPIO.setup(resistor_pin, GPIO.OUT)
		GPIO.output(resistor_pin, GPIO.LOW)
		time.sleep(0.1)

		GPIO.setup(resistor_pin, GPIO.IN)
		ct = time.time()
		diff = 0

		while GPIO.input(resistor_pin) == GPIO.LOW:
			diff = time.time() - ct
		
		
		if (diff*1000) > thresh:
			print("smile in 2 seconds")
			time.sleep(2)
			temp = subprocess.Popen([cmd, "-w", "500", "-h", "500", "-o", "temp.jpg"], stdout=subprocess.PIPE)
			temp.communicate()
			files = {"image": open("temp.jpg", "rb")}
			os.remove("temp.jpg")
			print("picture taken")
			response = requests.put(api, files=files)
			print(response.text)
			time.sleep(5)
except Exception as e:
	print("Error: ", e)

finally:
	GPIO.cleanup()
