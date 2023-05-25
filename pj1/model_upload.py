# upload model.pkl to google cloud storage
import os
from google.cloud import storage
from io import StringIO
import io
import pandas as pd
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Gcredentials.json"
client = storage.Client()
bucket = client.get_bucket("webscraping_446_hw2")

# Create a blob object for the csv file in the bucket
blob = bucket.blob('machinelearning/model.pkl')

blob.upload_from_filename("model.pkl")

print("File 'model.pkl' uploaded to 'machinelearning/model.pkl'.")
