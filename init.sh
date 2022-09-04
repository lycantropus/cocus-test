#!/bin/bash

cp ./src/.env.example ./src/.env

cp ./infra/aws.auto.tfvars.example ./infra/aws.auto.tfvars

ROOT=$(pwd)

cd "$ROOT/infra" && terraform init

cd "$ROOT/src" && pip install -r requirements.txt && pip install --target . --python 3.9 --only-binary=:all: -r requirements.txt 