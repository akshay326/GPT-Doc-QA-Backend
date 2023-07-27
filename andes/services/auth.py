from flask_httpauth import HTTPTokenAuth
import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='us-west-1')

auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(api_key):
    # Get an item from the table
    response = dynamodb.get_item(
        TableName='ANDES_API_KEYS',
        Key={
            'api_key': {'S': api_key}
        }
    )

    # Check if the item exists in the table
    return 'Item' in response
