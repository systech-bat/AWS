#!/bin/bash

aws iam create-role --role-name SSM02 --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "ec2.amazonaws.com",
          "ssm.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}'

aws iam attach-role-policy --role-name SSM02 --policy-arn arn:aws:iam::aws:policy/service-role/AmazonSSMAutomationRole

iamRoleArn="arn:aws:iam::562464429819:role/SSM02"

aws iam put-role-policy --role-name "SSM02" \
 --policy-name AllowPassRole \
 --policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "'$iamRoleArn'"
    }
  ]
}'

echo $iamRoleArn


aws configservice put-config-rule --config-rule '{
  "ConfigRuleName": "approved-amis-by-id",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "APPROVED_AMIS_BY_ID"
  },
  "InputParameters": "{\"amiIds\":\"ami-0e872aee57663ae2d\"}"
}'


aws configservice put-remediation-configurations --cli-input-json file://remediation_rule.json
