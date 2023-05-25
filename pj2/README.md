**This project is about using google cloud function and google cloud scheduler to automated webscraping data from apartments.com**

**Step 1**: Deploy google cloud function using "cloud_function_webscraping.py", "requirements.txt", "Gcredentials.json".

**Steo 2**: Try to call the function demo.

**Step 3**: Because we want to build an automated webscraping system, we need to make sure we store our data in google cloud buckets and replace it each time we run the cloud function to do the webscraping.

**Step 4**: Using the Cloud Scheduler to automated run the Cloud Function and update data in Cloud Buckets.
