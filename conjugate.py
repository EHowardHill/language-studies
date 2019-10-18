import requests, json

response = requests.get("https://api.verbix.com/finder/json/<apikey>/<version>/<language>/<verb>")
print(response.json())