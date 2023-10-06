# fix_CIDR_net
## Description
This script will run through all selected sites looking for site variables ending in _ip_cidr. Once found a new varible without the _ip_cidr and without the netmask will be created and pushed to the site. You will have the option to view all new variables before pushing to mist. This script **does not** delete any variables, it simply adds new ones.
## Requirements:
Ensure that you have python 3 and the [mistapi](https://pypi.org/project/mistapi/) package installed.
## Usage:
It is recommended, but not necessary, that you set up a file named mist_env containing your token like the below example:
```
MIST_HOST = api.mist.com
MIST_APITOKEN = xxxxxx
```
To use simply run fix_CIDR_net.py
