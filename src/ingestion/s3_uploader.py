"""Save API response data directly to S3 as JSON."""

import json

import boto3


class S3Uploader:
    """Save raw API response data in the S3 landing zone."""

    def __init__(self, bucket, prefix="raw"):
        self.bucket = bucket
        self.prefix = prefix.strip("/")
        self._client = boto3.client("s3")

    def upload_json(self, data, object_key):
        full_key = self.prefix + "/" + object_key
        json_text = json.dumps(data)
        json_bytes = json_text.encode("utf-8")
        self._client.put_object(
            Bucket=self.bucket,
            Key=full_key,
            Body=json_bytes,
            ContentType="application/json",
        )
        return full_key
