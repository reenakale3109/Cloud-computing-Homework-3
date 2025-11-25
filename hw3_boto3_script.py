import boto3
from botocore.exceptions import ClientError
REGION = "us-east-1"
BUCKET_NAME = "reena-hw1-bucket-2025"   
TABLE_NAME = "hw3-demo-table"


def list_s3_objects():
    """
    List all files in the specified S3 bucket.
    """
    s3 = boto3.client("s3", region_name=REGION)
    print(f"Listing objects in S3 bucket: {BUCKET_NAME}")
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        contents = response.get("Contents", [])
        if not contents:
            print("Bucket is empty.")
        else:
            for obj in contents:
                print(f"- {obj['Key']} ({obj['Size']} bytes)")
    except ClientError as e:
        print("Error listing S3 objects:", e)


def create_dynamodb_table():
    """
    Create a DynamoDB table if it does not exist.
    """
    dynamodb = boto3.client("dynamodb", region_name=REGION)

    try:
        print(f"Creating DynamoDB table: {TABLE_NAME}")
        response = dynamodb.create_table(
            TableName=TABLE_NAME,
            AttributeDefinitions=[
                {"AttributeName": "ID", "AttributeType": "S"}
            ],
            KeySchema=[
                {"AttributeName": "ID", "KeyType": "HASH"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )
    
        waiter = dynamodb.get_waiter("table_exists")
        waiter.wait(TableName=TABLE_NAME)
        print("DynamoDB table created successfully.")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"Table '{TABLE_NAME}' already exists.")


def insert_item():
    """
    Insert an item into the DynamoDB table.
    """
    dynamodb = boto3.client("dynamodb", region_name=REGION)
    print(f"Inserting item into table: {TABLE_NAME}")
    try:
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                "ID": {"S": "1"},
                "Name": {"S": "Reena"},
                "Assignment": {"S": "HW3 Boto3 demo"},
                "Score": {"N": "100"}
            }
        )
        print("Item inserted successfully.")
    except ClientError as e:
        print("Error inserting item:", e)


if __name__ == "__main__":
    print("=== Step 1: List S3 Objects ===")
    list_s3_objects()
    print("\n=== Step 2: Create DynamoDB Table ===")
    create_dynamodb_table()
    print("\n=== Step 3: Insert Item into DynamoDB ===")
    insert_item()
    print("\nAll Boto3 operations completed.")
