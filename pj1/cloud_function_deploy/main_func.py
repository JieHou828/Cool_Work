# remember to change the endpoint to main
import os
from google.cloud import storage
import joblib
from flask import jsonify, abort
import numpy as np
import logging
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def load_model_from_gcs(bucket_name, blob_name):
    """Load a model from Google Cloud Storage."""
    # Get the client
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Gcredentials.json"
    client = storage.Client()
    # Get the bucket
    bucket = client.get_bucket(bucket_name)
    # Get the blob
    blob = bucket.blob(blob_name)
    # Check if the blob exists
    if blob.exists():
        # Download the blob to a file
        blob.download_to_filename('/tmp/model.pkl')
    else:
        print("Blob does not exist")
        return None
    # Load the model
    model = joblib.load('/tmp/model.pkl')
    return model

def process_request(request):
    """Process a request to get the instance."""
    # Check if it's a POST request
    if request.method != 'POST':
        abort(405, 'Method not allowed')
    # Get the JSON data from the request
    data = request.get_json()
    # Check if 'instance' is in the data
    if 'instance' not in data:
        abort(400, 'Missing instance parameter')
    instance = data['instance']
    # Check that 'instance' is a list of length 8
    if not isinstance(instance, list) or len(instance) != 8:
        abort(400, 'Instance should be a list of length 8')
    # Convert instance to numpy array and reshape it to a 2D array
    instance = np.array(instance).reshape(1, -1)
    return instance

def predict(model, instance):
    """Make a prediction using the model and instance."""
    # Make prediction
    prediction = model.predict(instance)
    return prediction.tolist()

def main(request):
    """Main function to handle requests."""
    # Load the model
    model = load_model_from_gcs("webscraping_446_hw2", "machinelearning/model.pkl")
    if model is None:
        return 'Model not found', 500
    logging.info("Get Model Succeed.")
    # Process the request
    instance = process_request(request)
    # Make prediction
    prediction = predict(model, instance)
    # Delete the model file
    model = None
    os.remove('/tmp/model.pkl')
    logging.info("Model file deleted.")
    # Return prediction
    return jsonify({'status': 'Predict Finished!', 'prediction': prediction})
