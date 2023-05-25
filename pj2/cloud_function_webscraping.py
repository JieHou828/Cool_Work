import os
from google.cloud import storage
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date
from io import StringIO
import io
import logging

def web_scraping():
    url = 'https://www.apartments.com/los-angeles-ca/'  # replace with your URL
    headers = {'User-Agent': 'Mozilla/5.0'}  # replace with your headers
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all apartment listings
    listings = soup.find_all('li', {'class':'mortar-wrapper'})

    data = []

    # Loop through each listing
    for listing in listings:
        try:
            name = listing.find('span', {'class': 'js-placardTitle title'}).text
            price = listing.find('p', {'class':'property-pricing'}).text
            beds_baths = listing.find('p', {'class':'property-beds'}).text
            location = listing.find('div', {'class': 'property-address js-url'}).text
        except:
            continue

        # Add to data
        data.append({
            'Name': name,
            'Price': price,
            'Beds/Baths': beds_baths,
            'Location': location,
            'Date': date.today()  # Add the current date
        })

    # Create DataFrame
    df_current = pd.DataFrame(data)
    return df_current

def df_check(df_current):
    # Create a client to access Google Cloud Storage
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
        df_previous = pd.read_csv(blob_string, index_col=False)
        df = pd.concat([df_previous, df_current])
    else:
        df = df_current

    return df



def upload(df):
    # Create a client to access Google Cloud Storage
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Gcredentials.json"
    client = storage.Client()
    bucket_name = "webscraping_446_hw2"

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    # Define the blob (which is like a 'file' in Google Cloud Storage)
    blob = bucket.blob('webscrap/apartments.csv')

    # Upload the DataFrame to the csv file in the bucket
    # This will replace the existing 'apartments.csv' if it already exists
    blob.upload_from_string(df.to_csv(index=False), 'text/csv')


def main(request):
    df_current = web_scraping()
    logging.info("Finished web_scraping.")
    df = df_check(df_current)
    logging.info("Finished df_check.")
    upload(df)
    logging.info("Finished Upload.")
    return 'Web scraping completed and data uploaded to Google Cloud Storage.', 200
