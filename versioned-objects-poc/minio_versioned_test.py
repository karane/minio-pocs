import boto3
from botocore.client import Config

# MinIO connection settings
MINIO_ENDPOINT = "http://localhost:9000"
ACCESS_KEY = "admin"
SECRET_KEY = "admin123"
BUCKET_NAME = "versioned-bucket"

def main():
    # Create client
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1"
    )

    # Create bucket if it does not exist
    try:
        s3.create_bucket(Bucket=BUCKET_NAME)
        print(f"Bucket {BUCKET_NAME} created.")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket {BUCKET_NAME} already exists.")

    # Enable versioning
    s3.put_bucket_versioning(
        Bucket=BUCKET_NAME,
        VersioningConfiguration={"Status": "Enabled"}
    )
    print("Versioning enabled.")

    # Upload multiple versions of the same file
    object_key = "test-object.txt"
    version_ids = []

    for i in range(3):
        body = f"File content version {i}".encode("utf-8")
        response = s3.put_object(Bucket=BUCKET_NAME, Key=object_key, Body=body)
        version_id = response.get("VersionId")
        version_ids.append(version_id)
        print(f"Uploaded version {i}, VersionId={version_id}")

    # List all versions of the object
    print("\nListing versions:")
    response = s3.list_object_versions(Bucket=BUCKET_NAME, Prefix=object_key)
    for v in response.get("Versions", []):
        print(f"- Key={v['Key']} VersionId={v['VersionId']} IsLatest={v['IsLatest']} Size={v['Size']}")

    # Download an older version
    print("\nDownloading version 0 (oldest)...")
    old_version_id = version_ids[0]
    response = s3.get_object(Bucket=BUCKET_NAME, Key=object_key, VersionId=old_version_id)
    content = response["Body"].read().decode("utf-8")
    print(f"Content of version 0: {content}")

    # === DELETE MARKER TEST ===
    print("\nDeleting latest version (creates delete marker)...")
    delete_response = s3.delete_object(Bucket=BUCKET_NAME, Key=object_key)
    delete_marker_version = delete_response.get("VersionId")
    print(f"Delete marker created with VersionId={delete_marker_version}")

    # Try to fetch without versionId (should fail)
    try:
        s3.get_object(Bucket=BUCKET_NAME, Key=object_key)
    except Exception as e:
        print(f"As expected, cannot get object without versionId after delete: {e}")

    # Restore by fetching an older version explicitly
    print("\nRestoring older version...")
    response = s3.get_object(Bucket=BUCKET_NAME, Key=object_key, VersionId=old_version_id)
    restored_content = response["Body"].read().decode("utf-8")
    print(f"Restored content from version {old_version_id}: {restored_content}")

    # List all versions again to confirm delete marker
    print("\nListing versions after delete:")
    response = s3.list_object_versions(Bucket=BUCKET_NAME, Prefix=object_key)
    for v in response.get("Versions", []):
        print(f"- Key={v['Key']} VersionId={v['VersionId']} IsLatest={v['IsLatest']} Size={v['Size']}")
    for d in response.get("DeleteMarkers", []):
        print(f"- DELETE MARKER: Key={d['Key']} VersionId={d['VersionId']} IsLatest={d['IsLatest']}")

if __name__ == "__main__":
    main()
