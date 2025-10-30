## Project description

A Flask application that allows you to view a list and open content stored in Google Cloud Bucket.
The app.py file is responsible for displaying the list and data in a web browser.
The gcs_manager file is responsible for transferring files from your local computer to the cloud service.

## Configuration

The application uses Google Cloud Storage and has not yet been published, so you need to configure it yourself to run it locally.
In addition, you need to create a virtual environment and an .env file containing the following variables: FLASK_SECRET_KEY, GOOGLE_CLOUD_PROJECT, GCS_BUCKET_NAME.
