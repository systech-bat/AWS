#how to use
secret.py --secret 'prod/aurora01' --region 'eu-central-1'

import boto3
import base64
import json
import argparse
from botocore.exceptions import ClientError


parser = argparse.ArgumentParser()
parser.add_argument("--secret", type = str, required=True)
parser.add_argument("--region", type = str, required=False)
args = parser.parse_args()


def get_secret(s,r):


    secret_name = s
    region_name = r

	#Create SM client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
	# Get secret
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':


            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
    else:
        # Decrypts secret by KMS CMK.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret) # returns the secret as dictionary
        else:
            # if secret in  base 64
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return json.loads(secret) # returns the secret as dictionary


def main():
    secret_name = args.secret
    region_name = args.region
    password=get_secret(secret_name,region_name)
    
    print("@@Result=" + str(password))

if __name__ == '__main__':
    main()
