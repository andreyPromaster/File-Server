import uuid
from azure.storage.blob import BlobServiceClient
from FileServer import settings


class AzureStorageManager:
    def __init__(self, name_container=None):
        self.blob_service_client = BlobServiceClient.from_connection_string(settings.CONNECTION_STRING_TO_AZURE_STORAGE)
        if name_container is None:
            self.container_name = self.__create_unique_string()
        else:
            self.container_name = name_container

    def create_container(self):
        self.blob_service_client.create_container(self.container_name)

    @staticmethod
    def __create_unique_string():
        return str(uuid.uuid4())

    def get_current_container(self):
        return self.container_name

    def upload_file_to_container(self, file, file_name):
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=file_name)

        # Upload the created file
        blob_client.upload_blob(file.read())

    def download_file_from_storage(self, container, file_name):
        blob_client = self.blob_service_client.get_blob_client(container=container, blob=file_name)
        data = blob_client.download_blob().readall()
        return data


