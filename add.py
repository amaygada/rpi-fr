import requests

api = "https://241d-2405-201-17-f0cc-b498-3c83-3820-1a9c.ngrok.io/api/"

files = {"image1": open("a.jpg", 'rb'), "image2": open("b.jpg", 'rb')}
data = {"name": "Sharda", "email": "sharda@gmail.com"}
response = requests.post(api, files=files, data = data)
print(response.text)
