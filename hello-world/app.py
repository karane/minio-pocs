import boto3
from botocore.client import Config

# MinIO settings
ENDPOINT = "http://localhost:9000"
ACCESS_KEY = "admin"
SECRET_KEY = "admin123"
BUCKET_NAME = "test-bucket"

# Connect to MinIO
s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1"
)

# 1. Create bucket
s3.create_bucket(Bucket=BUCKET_NAME)

# 2. Upload a file
s3.put_object(Bucket=BUCKET_NAME, Key="hello.txt", Body="Hello MinIO!")

# 3. List objects
objects = s3.list_objects_v2(Bucket=BUCKET_NAME)
print("Objects in bucket:")
for obj in objects.get("Contents", []):
    print("-", obj["Key"])

# 4. Download file
response = s3.get_object(Bucket=BUCKET_NAME, Key="hello.txt")
print("Downloaded content:", response["Body"].read().decode())
