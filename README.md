# weblate-demo

Prerequisites:
boto

Before running any of the playbooks export these environment variables

```bash
export EC2_ACCESS_KEY=yourawsaccesskey
export EC2_SECRET_KEY=yourawssecretkey
export EC2_REGION=yourawsregion
```

Put ssh key in the same directory with master.yml

To create cloudformation stack run
```bash
ansible-playbook cloudformation.yml -vvvv
```
To delete stack
```bash
ansible-playbook cloudformation.yml -vvvv -e "delete_stack=true"
```
To configure weblate run
```bash
ansible-playbook -i inventory.py --private-key weblate.pem webservers.yml -e "generate_assets=true" --ask-vault-pass
```
Selinux is disabled by default
Some kind of a fix is
```bash
grep nginx /var/log/audit/audit.log | audit2allow -M nginx
semodule -i nginx.pp
```
taken from http://axilleas.me/en/blog/2013/selinux-policy-for-nginx-and-gitlab-unix-socket-in-fedora-19/
