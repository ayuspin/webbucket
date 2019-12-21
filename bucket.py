from google.cloud import storage


class BucketManager:
    """Class for bucket's operations."""

    def __init__(self):
        self.storage_client = storage.Client()

    def list_buckets(self):
        """List all buckets"""
        buckets = self.storage_client.list_buckets()
        for b in buckets:
            print(b.name)

    def list_bucket_objects(self, bucket_name):
        """List all objects for a bucket"""
        bucket = self.storage_client.get_bucket(bucket_name)
        objects_list = list(self.storage_client.list_blobs(bucket))
        for obj in objects_list:
            print(obj.name)
