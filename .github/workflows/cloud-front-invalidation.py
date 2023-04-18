#!/usr/bin/env python

"""
This script run invalidation for a given cloudFront distribution

Input:
    aws providers - access and secret keys and region
    the id of the distribution you want to run the invalidation on and path to the file for the invalidation

Output:
    new invalidation
"""

import argparse
import boto3


def get_arg():
    """
    get all user inputs
    """
    parser = argparse.ArgumentParser(description="Get user data")
    parser.add_argument('-aa', '--awsAccess', action='store', required=True, help='aws access key')
    parser.add_argument('-as', '--awsSecret', action='store',  required=True, help='aws secret key')
    parser.add_argument('-ta', '--awsRegion', action='store',  required=True, help='aws region where your distribution located')
    parser.add_argument('-di', '--distributionId', action='store',  required=True, help='path to work dir')
    parser.add_argument('-ip', '--invalidationPath', action='store',  required=True, help='the path of the file you want to run the distribution on')
    parser.add_argument('-in', '--invalidationName', action='store',  required=True, help='unique name for the current invalidation')

    args = parser.parse_args()

    return args

def create_invalidation (accessKey: str, secretKey: str, region: str, distributionId: str, invalidationPath: str, invalidationName: str):
    """
    create cloudfront invalidation
    :param awsAccessKey:
    :param awsSecretKey:
    :param awsRegion:
    :parm distributionId:
    :param invalidationPath:
    """
    # start boto3 session
    awsSession = boto3.Session( aws_access_key_id=accessKey, aws_secret_access_key=secretKey, region_name=region)
    # get cloudfront resource
    cloudfront = awsSession.client('cloudfront')
    # create invalidation
    response = cloudfront.create_invalidation( DistributionId=distributionId,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': [invalidationPath]
            },
            'CallerReference': invalidationName
        }
    )

    print(response)


def main():
    # get user input
    args = get_arg()
    # create invalidation
    create_invalidation (args.awsAccess, args.awsSecret, args.awsRegion, args.distributionId, args.invalidationPath, args.invalidationName)


if __name__ == '__main__':
    main()
