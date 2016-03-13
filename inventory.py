#!/usr/bin/env python
import subprocess
import json
import argparse
import sys
import os
# import yaml
import boto
from boto import ec2

aws_access_key = os.environ['EC2_ACCESS_KEY']
aws_secret_key = os.environ['EC2_SECRET_KEY']
aws_region = os.environ['EC2_REGION']

# with open("./group_vars/"+env, 'r') as ymfile:
#     cfg = yaml.load(ymfile)
con =  ec2.connect_to_region(aws_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)

def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    return parser.parse_args()

def host_list():
    host_vars = {}
    ansible_hosts = {}
    for res in con.get_all_instances():
        for inst in res.instances:
            if inst.state == "running": # TODO change this to filter in API requests
                # Add dict values with instance id and ip address for ssh
                ssh_host = {"ansible_ssh_host" : inst.ip_address}
                host = {inst.id : ssh_host}
                host_vars.update(host)

                # Form group lists with instance id's
                try:
                    ansible_hosts[inst.tags['group']].append(inst.id)
                except: # if host group doesn't exist
                    ansible_hosts.update({inst.tags['group']: []})
                    ansible_hosts[inst.tags['group']].append(inst.id)
    # Make final inventory list
    ansible_hosts.update({
        "_meta" : {
            "hostvars": host_vars
        }
    })

    return(ansible_hosts)


def main():
    args = parse_args()
    if args.list:
        json.dump(host_list(), sys.stdout)

if __name__ == '__main__':
    main()
