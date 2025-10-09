from google.cloud import storage
import os
import logging
import argparse

base_dir = os.path.dirname(os.path.abspath(__file__))  # folder where gsc_manager.py lives
path_log = os.path.join(base_dir, "logs", "simple_back_end.log")
if not os.path.exists(os.path.dirname(path_log)):
    os.makedirs(os.path.dirname(path_log))
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                    filename=path_log, 
                    filemode='a')

#Authorization
credentials_path = os.path.join(base_dir, "secrets", "cloude-file-storage.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
client = storage.Client()
bucket_name = "storage-for-text-files"
bucket = client.bucket(bucket_name)

def upload_to_gcs(filename: str, content: str) -> None:
    blob = bucket.blob(filename)
    blob.upload_from_string(content, content_type="text/plain")
    logging.info(f"Uploaded {filename} to {bucket_name}.")

def download_to_gcs(filename: str):
    blob = bucket.blob(filename)
    logging.info(f"Downloaded {filename} from {bucket_name}.")
    return blob.download_as_text()    

parser = argparse.ArgumentParser(description="GCS File Manager")
subparsers = parser.add_subparsers(dest = "command")
upload_parser = subparsers.add_parser("upload", help="Upload a file to GCS")
upload_parser.add_argument("file_path", type=str, help="Path to the file to upload")   
download_parser = subparsers.add_parser("download", help="Download a file from GCS")
download_parser.add_argument("local_path", type=str, help="Local path to save the downloaded file")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.command == "upload":
        try:
            with open(args.file_path, 'r') as file:
                content = file.read()
            upload_to_gcs(os.path.basename(args.file_path), content)
            logging.info(f"File {args.file_path} uploaded successfully.")
        except Exception as e:
            logging.error(f"Error uploading file {args.file_path}: {e}")
    elif args.command == "download":
        try:
            content = download_to_gcs(os.path.basename(args.local_path))
            with open(args.local_path, 'w') as file:
                file.write(content)
            print(f"File downloaded and saved to {args.local_path}.")
        except Exception as e:
            logging.error(f"Error downloading file to {args.local_path}: {e}")
            print(f"Failed to download file: {e}")
    else:
        parser.print_help()