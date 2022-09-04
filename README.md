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
Simply run the following command from the root folder.
```
python src/run.py name=*
```

a name parameter should be passed to apply the filter

### Lambda Function

In order to deploy the resources just run:
```
cd infra && terraform apply --auto-approve
```
After this, a test event can be created in the AWS console.
This test event should consist of a JSON object with a name key and a value which will be the filter:
```JSON
{
    "name": "*"
}
```
Press Test and you should see the result in the log display.

