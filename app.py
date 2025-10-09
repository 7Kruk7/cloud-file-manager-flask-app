from flask import Flask, jsonify, request, redirect, url_for, session
from flask_cors import CORS
from google.cloud import storage
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import os
import logging


base_dir = os.path.dirname(os.path.abspath(__file__))  # folder where gsc_manager.py lives
path_log = os.path.join(base_dir, "logs", "simple_back_end.log")
if not os.path.exists(os.path.dirname(path_log)):
    os.makedirs(os.path.dirname(path_log))
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                    filename=path_log, 
                    filemode='a')
app = Flask(__name__)
CORS(app)

credentials_path = os.path.join(base_dir, "secrets", "cloude-file-storage.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
client = storage.Client()
bucket_name = "storage-for-text-files"
bucket = client.bucket(bucket_name)

@app.route('/', methods=['GET'])
def display_files():
    try:
        blobs = bucket.list_blobs()
        files = [blob.name for blob in blobs]
        logging.info("Files retrieved successfully.")
        return jsonify({"files": files}), 200
    except Exception as e:
        logging.error(f"Error retrieving files: {e}")
        return jsonify({"error": "Could not retrieve files"}), 500
    
@app.route('/<filename>', methods=['GET'])
def get_file_content(filename):
    try:
        blob = bucket.blob(filename)
        if not blob.exists():
            logging.warning(f"File {filename} not found.")
            return jsonify({"error": "File not found"}), 404
        content = blob.download_as_text()
        logging.info(f"File {filename} retrieved successfully.")
        return jsonify({"filename": filename, "content": content}), 200
    except Exception as e:
        logging.error(f"Error retrieving file {filename}: {e}")
        return jsonify({"error": "Could not retrieve file"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)