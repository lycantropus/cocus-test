import sys
from ebs_describe import main

def lambda_handler(event, context):
    name_filter = event['name']

    if(name_filter == ''):
        print('Missing name key from event')
        return sys.exit(1)
    main(name_filter)