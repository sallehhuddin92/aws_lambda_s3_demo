import boto3
import uuid
from PIL import Image
from urllib.parse import unquote_plus
            
s3_client = boto3.client('s3')
            
def create_thumbnail(image_path, thumbnail_path):
  with Image.open(image_path) as image:
    image.thumbnail(tuple(x / 2 for x in image.size))
    image.save(thumbnail_path)
            
def lambda_handler(event, context):
  for record in event['Records']:
    bucket = record['s3']['bucket']['name']
    key = unquote_plus(record['s3']['object']['key'])
    tmpkey = key.replace('/', '')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
    upload_path = '/tmp/thumbnail-{}'.format(tmpkey)
    s3_client.download_file(bucket, key, download_path)
    create_thumbnail(download_path, upload_path)
    s3_client.upload_file(upload_path, '{}-thumbnail'.format(bucket), 'thumbnail-{}'.format(key))