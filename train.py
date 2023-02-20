import base64
import json
import requests

api = "https://241d-2405-201-17-f0cc-b498-3c83-3820-1a9c.ngrok.io/api/"

response = requests.get(api)
print(response.text)
