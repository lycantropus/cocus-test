provider "aws" {
  region = "${var.region}"
}


resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

data "archive_file" "lambda_zip" {
    type        = "zip"
    source_dir  = "../src"
    output_path = "lambda.zip"
}

resource "aws_lambda_function" "test_lambda" {
  filename      = "lambda.zip"
  function_name = "lambda_function_ebs"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "main.main"

  source_code_hash = "${data.archive_file.lambda_zip.output_base64sha256}"

  runtime = "python3.9"

  environment {
    variables = {
      # aws_access_key_id = var.aws_access_key_id,
      # aws_secret_access_key = var.aws_secret_access_key
      # region = var.region
    }
  }
}