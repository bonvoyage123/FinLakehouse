import json
from pathlib import Path

import boto3


class S3Uploader:
    """Upload raw JSON payloads to an S3 landing zone."""

    def __init__(self, bucket, prefix="raw"):
        self.bucket = bucket
        self.prefix = prefix.strip("/")
        self._client = boto3.client("s3")

    def upload_json(self, data, object_key):
        full_key = self.prefix + "/" + object_key
        self._client.put_object(
            Bucket=self.bucket,
            Key=full_key,
            Body=json.dumps(data).encode("utf-8"),
            ContentType="application/json",
        )
        return full_key

    def upload_file(self, file_path, object_key):
        source = Path(file_path)
        full_key = self.prefix + "/" + object_key
        self._client.upload_file(str(source), self.bucket, full_key)
        return full_key
