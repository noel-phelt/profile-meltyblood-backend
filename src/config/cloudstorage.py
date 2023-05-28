import uuid

from fastapi import UploadFile
from google.cloud import storage
from google.oauth2 import service_account

from config.env import FIREBASE_CERT, GCP

credential = service_account.Credentials.from_service_account_info(
    FIREBASE_CERT)


class CloudStorage:
    def __init__(self):
        self.client = storage.Client(
            project=GCP['project_id'], credentials=credential)
        self.bucket = self.client.get_bucket(GCP['bucket_name'])

    def upload_profile(self, profile_image: UploadFile) -> str:
        file_name = str(uuid.uuid4()) + ".png"
        path = 'profiles/' + file_name
        blob_storage = self.bucket.blob(path)
        blob_storage.upload_from_file(
            profile_image.file, content_type=profile_image.content_type)

        return file_name

    def delete_profile(self, image_path: str):
        self.bucket.delete_blob('profiles/' + image_path)
