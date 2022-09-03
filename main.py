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

        


def main():
    
    if(not passed_config_check()):
        return sys.exit(1)

    if(not sys.argv[1].startswith('name=')):
        print('A name argument should be passed. Use * if you want to get all EC2 instances')
        print_usage()
        return sys.exit(1)
    
    instance_name_filter = sys.argv[1].replace('name=', '')
    if(instance_name_filter == ''):
        print('no filter passed to name argument. Please use an instance name or * for all instances')
        print_usage()
        return sys.exit(1)

    ec2_client = boto3.resource('ec2',
        aws_access_key_id=os.environ.get('aws_access_key_id'),
        aws_secret_access_key=os.environ.get('aws_secret_access_key'),
        region_name=os.environ.get('region'))

    instances = {}

    match instance_name_filter:
        case '*':
            instances = ec2_client.instances.all()
        case _:
            instances = ec2_client.instances.filter(Filters=[
                    {
                        'Name': 'tag:Name',
                        'Values': [instance_name_filter]
                    }
                ]
            )

    total_volume_size = 0
    instances_data = []
    
    for instance in instances:
        print(instance.tags)
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

main()