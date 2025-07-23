"""
Service for automatically updating the airport data periodically
"""

import os
import json
import boto3
from helpers.fr24_api import get_all_airports

BUCKET_NAME = os.getenv("BUCKET_NAME")
s3_client = boto3.client("s3")


def lambda_handler(event, context):
    airports = get_all_airports().get("rows")

    if len(airports) == 0:
        raise ValueError("Airport list is empty")

    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key="airports.json",
        Body=json.dumps(airports),
        ContentType="application/json",
    )

    return {"statusCode": 200, "body": "Airports were updated successfully"}
