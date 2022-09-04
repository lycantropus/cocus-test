from dotenv import load_dotenv
from tabulate import tabulate
import boto3
import os
import sys
load_dotenv()

def print_usage():
    print('ex: ' + sys.argv[0] + ' name=exampleinstance')
    print('ex: ' + sys.argv[0] + ' name=*')

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

def print_table(instances_data):
    headers = instances_data[0].keys()
    data = [data.values() for data in instances_data]
    print(tabulate(data, headers))

    
def main(name_filter):
    
    if(not passed_config_check()):
        return sys.exit(1)   

    ec2_client = boto3.resource('ec2',
        aws_access_key_id=os.environ.get('aws_access_key_id'),
        aws_secret_access_key=os.environ.get('aws_secret_access_key'),
        region_name=os.environ.get('region'))

    #ec2_client = boto3.resource('ec2')

    instances = {}

    # only for python3.10
    # match instance_name_filter:
    #     case '*':
    #         instances = ec2_client.instances.all()
    #     case _:
    #         instances = ec2_client.instances.filter(Filters=[
    #                 {
    #                     'Name': 'tag:Name',
    #                     'Values': [name_filter]
    #                 }
    #             ]
    #         )

    if(name_filter == '*'):
        instances = ec2_client.instances.all()
    else:
        instances = ec2_client.instances.filter(Filters=[
                    {
                        'Name': 'tag:Name',
                        'Values': [name_filter]
                    }
                ]
            )  

    total_volume_size = 0
    instances_data = []
    if(len([instance for instance in instances]) == 0):
        print('No EC2 server found for that name')
        return sys.exit(1)
    
    for instance in instances:
        instance_volumes = instance.volumes.all()
        instance_volumes_size = 0

        for instance_volume in instance_volumes:
            instance_volumes_size += instance_volume.size

        total_volume_size += instance_volumes_size
        
        instances_data.append({
            'instance-id': instance.id,
            'instance-type': instance.instance_type,
            'status': instance.state['Name'],
            'private-ip': instance.private_ip_address,
            'public-ip': instance.public_ip_address,
            'total-size-ebs-volumes': instance_volumes_size
        })
    instances_data.sort(key=lambda x:x['total-size-ebs-volumes'], reverse=True)

    print_table(instances_data)
    print('\nTotal EBS size: ' + str(total_volume_size) + 'GB')


