# hello-world web app:

This repo contains all the files and scripts required in order to create a simple web app, which is hosted in an AWS S3 bucket, and distributed by AWS CloudFront.

## Repo structure:
The repo contain folders:
1. infra: holds all the files and scripts which required to preper AWS env for the web app.
2. app-contanct- contains a simple index.html, which the app will "publish".

In addition, the repo contains the .github folder, which contains the git-action scripts, that enable automatic upgrade and deployment.

### AWS pre requirements:
The scripts assuming you already have in your AWS account the following recurses:
1. AMI user with permissions to create all the resurces in the terraform modules, to update the web-app s3 buacket, and with aws cli access (access and secret keys).
2. dynamoDB dynamodb-table - to mange terraform workcpases.
3. s3 bucket, to hold the tf.state files.

### Github pre requirements:
1. secret named AWS_ACCESS_KEY_ID which hold an aws access key for user with permissions to update the webbapp bucket.
2. secret named AWS_SECRET_ACCESS_KEY which hold an aws secret key for user with permissions to update the webbapp bucket.
3. secret named AWS_REGION which holds the AWS's region "code" (for example eu-est-1) where your resources are located.
4. secret named WEB_APP_BUCKET_NAME which holds the bucket name where the web-app files located.

### Upgrade flow
Every push to "main" branch will upload the index.html, from main branch, to the webapp bucket.
Note: The upgrade flow will pass only the webapp's S3 bucket was created.