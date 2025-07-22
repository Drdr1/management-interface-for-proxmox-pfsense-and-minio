from minio import Minio

MINIO_HOST = '192.168.1.5:9000'
MINIO_ACCESS_KEY = 'galagant'
MINIO_SECRET_KEY = 'galagant'

minio_client = Minio(MINIO_HOST, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=False)

def minio_list_buckets():
    return [bucket.name for bucket in minio_client.list_buckets()]

def minio_create_bucket(params):
    bucket_name = params.get('bucket_name')
    region = params.get('region', 'us-east-1')
    minio_client.make_bucket(bucket_name, location=region)
    return {'status': 'bucket created', 'bucket': bucket_name}
