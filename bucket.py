from google.cloud import storage
from pathlib import Path


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

    def setup_bucket(self, bucket_name):
        """Creates a bucket and makes it public"""
        bucket = self.storage_client.lookup_bucket(bucket_name)
        if not bucket:
            bucket = self.storage_client.create_bucket(bucket_name)
            print('Bucket {} created.'.format(bucket.name))
            bucket.configure_website("index.html", "404.html")
            bucket.make_public(recursive=True, future=True)
            print('Bucket {} made public.'.format(bucket.name))

    @staticmethod
    def files_for_blobs(path):
        """Get files for upload as blobs"""
        blobs = {}
        path = Path(path)
        for p in list(path.glob('**/*')):
            if not p.is_dir():
                abs_path = str(p.resolve())
                blob_name = str(p.resolve().relative_to(path.resolve()))
                blobs[blob_name] = abs_path
        return blobs

    def sync_bucket(self, path, bucket_name):
        """Upload files to a bucket"""
        blobs = self.files_for_blobs(path)
        bucket = self.storage_client.lookup_bucket(bucket_name)
        base_url = 'https://storage.googleapis.com/'
        if bucket:
            for b in blobs:
                blob = bucket.blob(b)
                blob.upload_from_filename(blobs[b])
                print('Uploaded {} to bucket {}.'.format(b, bucket_name))
            print(('You can access bucket webpage at '
                   '{}{}/index.html'.format(base_url, bucket_name)))
        else:
            print('Bucket {} does\'t exist.'.format(bucket_name))
