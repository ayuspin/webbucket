"""Script to create website based on GCP Storage bucket."""

import click
from bucket import BucketManager

bucket_manager = BucketManager()


@click.group()
def cli():
    pass


@cli.command()
def list_buckets():
    bucket_manager.list_buckets()


@cli.command()
@click.argument('bucket_name')
def list_bucket_objects(bucket_name):
    bucket_manager.list_bucket_objects(bucket_name)


@cli.command()
@click.argument('bucket_name')
def setup_bucket(bucket_name):
    bucket_manager.setup_bucket(bucket_name)


@cli.command()
@click.argument('path')
@click.argument('bucket_name')
def sync_bucket(path, bucket_name):
    bucket_manager.sync_bucket(path, bucket_name)


if __name__ == '__main__':
    cli()
