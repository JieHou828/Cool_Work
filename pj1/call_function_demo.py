import requests
import json

# Define the URL of the web service
url = "https://us-west2-webscrapingml.cloudfunctions.net/hw2-3_machinelearning"

# Define the instance for which you want to make a prediction
instance = [3.5, 20, 5, 1, 1000, 3, 35.631861, -119.569704]

# Make the POST request
response = requests.post(url, json={'instance': instance})
# print(response.text)
# Print the prediction
print(json.loads(response.text)['prediction'])
