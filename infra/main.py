#!/usr/bin/env python

"""
This script creates aws env for hello-world app

Input:
    aws providers - access and secret keys
    workspace - path to the work dir
    the terafrom action you want to run - apply/destroy

Output:
    new env which inclouds: S3 bucket and cloudFront
"""

import argparse
import json
import subprocess


def get_arg():
    """
    get all user inputs
    """
    parser = argparse.ArgumentParser(description="Get user data")
    parser.add_argument('-aa', '--awsAccess', action='store', required=True, help='aws access key')
    parser.add_argument('-as', '--awsSecret', action='store',  required=True, help='aws secret key')
    parser.add_argument('-ta', '--tfAction', action='store',  required=True, help='the terraform action cmd you want to run apply/destroy')
    parser.add_argument('-wc', '--workspace', action='store',  required=True, help='path to work dir')

    args = parser.parse_args()

    return args

def create_json (args, jsonVars):
    """
    create jeson file from given keys and values
    :param args:
    :param jsonVars: output json name
    :return:
    """
    # create py dictionary from user input
    varsDictionary = {}
    varsDictionary ["access_key"] = args.awsAccess
    varsDictionary ["secret_key"] = args.awsSecret

    print ("create json vars for tf")
    with open(f"{args.workspace}/{jsonVars}", 'w', encoding='utf-8') as f:
        json.dump(varsDictionary, f, ensure_ascii=False, indent=4)

    
def run_terraform (workspace: str, jsonVars: str, accessKey: str, secretKey: str , tfWorkspace: str, tfAction: str):
    """
    create uvis env in AWS using tarrform
    :param workspace
    :parm jsonVars: path to the json file which contain the tarrdorm vars
    :parm accessKey: aws access key
    :parm secretKey: aws secret key
    :return:
    """
    # set terraform cmd
    terraformCmd = f"docker run --rm -i --privileged -u root -v {workspace}:/opt/data yisca/terraform-crt:1.1.2 -chdir=/opt/data/{workspace}"
    s3Creds= f"-backend-config='access_key={accessKey}' -backend-config='secret_key={secretKey}'"
    
    # init terraform env
    res = subprocess.call (f"{terraformCmd} init -upgrade {s3Creds}", shell=True)
    if res != 0:
        raise SystemExit('failed to init terraform env, script returm exit code {0}'.format (res))
    else:
        print (f"terraform init successed")

    # check if workcapse exist and if not - create one
    getWorkcpace = subprocess.check_output (f"{terraformCmd} workspace list", shell=True)
    # conver to binary
    tfWorkspace_binary = b"" + tfWorkspace.encode('utf-8')
    if not tfWorkspace_binary in getWorkcpace:
        res = subprocess.call (f"{terraformCmd} workspace new {tfWorkspace}", shell=True)
        if res != 0:
            raise SystemExit('failed to create terraform workspace, script returm exit code {0}'.format (res))
        else:
            print (f"new workspace was created")

    # select workspace
    res = subprocess.call (f"{terraformCmd} workspace select {tfWorkspace}", shell=True)
    if res != 0:
        raise SystemExit('failed to select terraform workspace, script returm exit code {0}'.format (res))
    else:
        print (f"workspace {tfWorkspace} selected")

    # run it
    res = subprocess.call (f"{terraformCmd} {tfAction} -auto-approve -var-file={jsonVars}", shell=True)
    if res != 0:
        raise SystemExit('failed to {0} terraform env, script returm exit code {1}'.format (tfAction,res))
    else:
        print (f"terraform {tfAction} end successfully")

def main():
    # get user input
    args = get_arg()
    # local args
    jsonVars = "vars.json"
    tfWorkspace = "hello-word-webapp"
    # create json of keys and values for terraform
    create_json (args, jsonVars)

    # run it
    run_terraform (args.workspace, jsonVars, args.awsAccess, args.awsSecret, tfWorkspace, args.tfAction)

if __name__ == '__main__':
    main()
