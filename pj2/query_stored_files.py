import os
from google.cloud import storage
from io import StringIO
import io
import pandas as pd
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Gcredentials.json"
client = storage.Client()
bucket_name = "webscraping_446_hw2"

# Get the bucket
bucket = client.get_bucket(bucket_name)

# Create a blob object for the csv file in the bucket
blob = bucket.blob('webscrap/apartments.csv')

# Check if the csv file exists in the bucket
if blob.exists():
    # Download the csv file to a DataFrame
    blob_string = io.StringIO(blob.download_as_string().decode('utf-8'))
    # Read the csv file into a DataFrame
    df_latest = pd.read_csv(blob_string, index_col=False)

display(df_latest)
