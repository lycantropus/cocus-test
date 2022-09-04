# COCUS DevOps Challenge

This repo stores the solution to the COCUS DevOps Challenge

## Environment
Python 3.8
Terraform 0.15.8

## Installation

For convenience a bash script ```init.sh``` was developed. 
The script must be ran from this repo root.
This script bootstraps the environment (initialized terraform modules, and installs python packages) and the required env files/variable files.

After initialitazion, the src/.env and infra/aws.auto.tfvars files must be configured with your credentials

## Usage

### Python Script

```
python src/run.py name=*
```

### Lambda Function

In order to deploy the resources just run:
```
terraform apply --auto-approve
```
After this, a test event can be created in the AWS console.
This test event should consist of a JSON object with a name key and a value which will be the filter:
```JSON
{
    "name": "*"
}
```

