# Call google cloud function
import requests
url = "https://us-west2-webscrapingml.cloudfunctions.net/hw2-2_webscraping"
response = requests.get(url)

# Print the response
print(response.text)
