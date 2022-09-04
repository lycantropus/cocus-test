from ebs_describe import main
import sys

def print_usage():
    print('ex: ' + sys.argv[0] + ' name=exampleinstance')
    print('ex: ' + sys.argv[0] + ' name=*')

def run():
    if(len(sys.argv)<2 or not sys.argv[1].startswith('name=')):
        print('A name argument should be passed. Use * if you want to get all EC2 instances')
        print_usage()
        return sys.exit(1)
    
    instance_name_filter = sys.argv[1].replace('name=', '')
    if(instance_name_filter == ''):
        print('no filter passed to name argument. Please use an instance name or * for all instances')
        print_usage()
        return sys.exit(1)
    main(instance_name_filter)


run()