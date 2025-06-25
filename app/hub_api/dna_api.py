from minio import Minio
import io

class MinioTenant:
    def __init__(self, endpoint, access_key = None, secret_key = None):
        self.minio_client = Minio(
            endpoint = endpoint,
            access_key = access_key,
            secret_key = secret_key,
            secure=False
        )
        

    def insert(self, file_data, bucket_name):
        result = self.minio_client.put_object(bucket_name = bucket_name, object_name = "blah",data=io.BytesIO(file_data), length = len(file_data))
        return result

