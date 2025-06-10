import os
import csv
import json
import time
from io import StringIO

import boto3
from clickhouse_driver import Client

MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT', 'minio:9000')
MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY', 'minioadmin')
MINIO_BUCKET = os.environ.get('MINIO_BUCKET', 'data')

CLICKHOUSE_HOST = os.environ.get('CLICKHOUSE_HOST', 'clickhouse')
CLICKHOUSE_PORT = int(os.environ.get('CLICKHOUSE_PORT', '9000'))
CLICKHOUSE_USER = os.environ.get('CLICKHOUSE_USER', 'default')
CLICKHOUSE_PASSWORD = os.environ.get('CLICKHOUSE_PASSWORD', '')
CLICKHOUSE_DB = os.environ.get('CLICKHOUSE_DB', 'default')

TABLE_NAME = 'ingestions'


def wait_for_minio():
    s3 = boto3.client(
        's3',
        endpoint_url=f'http://{MINIO_ENDPOINT}',
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )
    while True:
        try:
            s3.list_buckets()
            break
        except Exception:
            time.sleep(1)
    return s3


def wait_for_clickhouse():
    client = Client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, user=CLICKHOUSE_USER, password=CLICKHOUSE_PASSWORD)
    while True:
        try:
            client.execute('SELECT 1')
            break
        except Exception:
            time.sleep(1)
    return client


def ensure_table(client):
    client.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id UInt64,
            ingestion_date DateTime,
            data_value String
        ) ENGINE = MergeTree() ORDER BY id
    """)


def process_csv_object(s3, client, obj_key):
    response = s3.get_object(Bucket=MINIO_BUCKET, Key=obj_key)
    body = response['Body'].read().decode('utf-8')
    reader = csv.DictReader(StringIO(body))

    rows = []
    for idx, row in enumerate(reader, start=1):
        json_value = json.dumps(row)
        rows.append({'id': idx, 'ingestion_date': int(time.time()), 'data_value': json_value})

    client.execute(f'INSERT INTO {TABLE_NAME} (id, ingestion_date, data_value) VALUES', rows)


def main():
    s3 = wait_for_minio()
    client = wait_for_clickhouse()
    ensure_table(client)

    if MINIO_BUCKET not in [b['Name'] for b in s3.list_buckets().get('Buckets', [])]:
        s3.create_bucket(Bucket=MINIO_BUCKET)
        # upload sample data if bucket was just created
        with open('/data/sample.csv', 'rb') as f:
            s3.upload_fileobj(f, MINIO_BUCKET, 'sample.csv')

    objects = s3.list_objects_v2(Bucket=MINIO_BUCKET).get('Contents', [])
    for obj in objects:
        process_csv_object(s3, client, obj['Key'])


if __name__ == '__main__':
    main()
