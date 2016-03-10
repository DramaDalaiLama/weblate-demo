#!/usr/bin/env python
import subprocess
import json
import argparse
import sys
import os
import yaml
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

# Now print out ansible-readable json
# def get_asg_tag(tag_name):
#     asg_tags = asg.get_all_tags()
#     for tag in asg_tags:
#         if tag.key == tag_name:
#             return tag.value

# Output must be dict
def host_vars():
    host_vars = {}
    for res in con.get_all_instances():
        for inst in res.instances:
            if inst.state == "running":
                ssh_host = {"ansible_ssh_host" : inst.ip_address}
                host = {inst.id : ssh_host}
                host_vars.update(host)
    return(host_vars)

# TODO: do something about this cycle in host_vars and host_list functions.

def host_group_list():
    host_group_list = []


# Output must be list
def host_list():
    host_list = []
    for res in con.get_all_instances():
        for inst in res.instances:
            if "type" in inst.tags.keys() and inst.state == "running":
                if inst.tags['type'] == cfg['environment_type']:
                    host = inst.id
                    host_list.append(host)
    return(host_list)

def host_vars():
    host_vars = {}
    host_groups = {}
    host_list = []
    ansible_hosts = {}
    for res in con.get_all_instances():
        for inst in res.instances:
            if inst.state == "running":
                # Add dict values with instance id and ip address for ssh
                ssh_host = {"ansible_ssh_host" : inst.ip_address}
                host = {inst.id : ssh_host}
                host_vars.update(host)

                # Form group lists with instance id's
                try:
                    host_groups.update({inst.tags['group']: {
                        "hosts": [].append(inst.id)             #make this idea work somehow
                    }})


    return(host_vars)


def main():
    args = parse_args()
    host_group = "cfg['client_name']+"-"+cfg['environment_type']
    h_list=host_list()
    ansible_hosts = {
        "_meta" : {
            "hostvars" : host_vars()
        },
        host_group : {
            "hosts" : h_lists
        }
    }
    if args.list:
        json.dump(ansible_hosts, sys.stdout)

if __name__ == '__main__':
    main()
