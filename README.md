# weblate-demo

Prerequisites:
boto

Before running any of the playbooks export these environment varibles

export EC2_ACCESS_KEY=yourawsaccesskey
export EC2_SECRET_KEY=yourawssecretkey
export EC2_REGION=yourawsregion

To create cloudformation stack run
'''bash
ansible-playbook -i 127.0.0.1, cloudformation.yml -vvvv
'''
To delete stack
'''bash
ansible-playbook -i 127.0.0.1, cloudformation.yml -vvvv -e "delete_stack=true"
'''
