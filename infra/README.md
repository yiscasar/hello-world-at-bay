# hello-world webapp - env terraform

### what it creates:
This module create ogen app infra. <br> 
After running the terrafom file, you will have an aws env with:
- 1 "web-app" bucket, which configured to host website.
- 1 cloudFront distribution, which connected to the web-app bucket. The cloudFront distribution includes ACA certificate and route 53 record.
- 1 ECS farget cluster.
- 1 postgres RDS.

## folder files:
- main.tf: terraform script, which creates vpc, subnet, route table and internet gateway
- var.tf: terraform variables file, which contains all the necessary variables in order for the main.tf
- backend.tf: terraform script which contains the defnion of tf.stat "backup" data - aws dynamodb table and s3 bucket name <br> <br>
- main.py: python script which "rape" all the procces, using user input

## Required input:
- aws_access_key
- aws_secret_key
- tfAction (apply/destroy)
- workspace: full path to the repo root folder, its most recomended to run it from the repo rot folder

## How to run ogen-network module:
In order to run this module, with the default values, pls run: <br>
`python3 $workspace/main.py --workspace <work dir> --awsAccess <aws_access_key> --awsSecret <aws_secret_key> --tfAction <tfAction>` <br>