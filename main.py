from dotenv import load_dotenv
import boto3
import os
load_dotenv()


def passed_config_check():
    missing_env_vars = [];
    if os.environ.get('aws_access_key_id') == None:
        missing_env_vars.append('aws_access_key_id')
    if os.environ.get('aws_secret_access_key') == None:
        missing_env_vars.append('aws_secret_access_key')
    if os.environ.get('region') == None:
        missing_env_vars.append('region')
    
    if(len(missing_env_vars)>0):
        print('Missing required environment variables: ' + ', '.join(missing_env_vars) + '.')
        return False

    return True

        


def main():
    
    if(not passed_config_check()):
        return
        
    ec2_client = boto3.client('ec2',
        aws_access_key_id=os.environ.get('aws_access_key_id'),
        aws_secret_access_key=os.environ.get('aws_secret_access_key'),
        aws_region=os.environ.get('region'))

    # instances = ec2_client.instances


main()