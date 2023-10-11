import UIToolsP3
import mistapi
import json
import os

env_file_path = "./mist_env"

def build_session():
    #Build session, preferably with env file
    if os.path.isfile(env_file_path):
        session = mistapi.APISession(env_file=env_file_path)
    else:
        print('Could not find mist_env file at '+env_file_path+'. Consider adding one to make log in easier')
        session = mistapi.APISession()
    return session


UIToolsP3.printHeader('Fix CIDR Net')
UIToolsP3.printSubHeader('Log into Mist')
mist_session = build_session()
mist_session.login()
UIToolsP3.printSubHeader('Select Org and Sites')
org_id = mistapi.cli.select_org(mist_session)[0]
site_ids = mistapi.cli.select_site(mist_session, org_id=org_id, allow_many=True)

print('Pulling site settings...')
problem_vars = {}
site_names = {}
for site_id in site_ids:
    site_settings = mistapi.api.v1.sites.setting.getSiteSetting(mist_session, site_id)
    site_info = mistapi.api.v1.sites.sites.getSiteInfo(mist_session, site_id)
    UIToolsP3.printSubHeader('Site: ' + site_info.data['name'])
    if 'vars' not in site_settings.data or not site_settings.data['vars']:
        print("Site "+site_info.data['name']+" has no vars")
        continue
    site_names[site_id] = site_info.data['name']
    problem_vars[site_id] = {}
    found_problem_vars = False
    for var in site_settings.data['vars']:
        if var.endswith('_ip_cidr'):
            found_problem_vars = True
            print('Found var: '+var+' with value: '+site_settings.data['vars'][var])
            problem_vars[site_id][var[:-8]] = {
                'Old var': {
                    'name': var,
                    'value': site_settings.data['vars'][var]
                },
                'New var': {
                    'name': var[:-8],
                    'value': site_settings.data['vars'][var].split('/')[0]
                }
            }
    if not found_problem_vars: print("Site "+site_info.data['name']+" has no problematic vars")

UIToolsP3.printSubHeader('Summary of vars to add')
print('Important! This script will not delete any vars, it just adds the new ones')
for site in problem_vars:
    if problem_vars[site]:
        print(site_names[site]+': ')
        for var in problem_vars[site]:
            print('    '+problem_vars[site][var]['Old var']['name']+': '+problem_vars[site][var]['Old var']['value']+' --> '
                  + problem_vars[site][var]['New var']['name']+': '+problem_vars[site][var]['New var']['value'])

if UIToolsP3.getBool('Continue? '):
    UIToolsP3.printSubHeader('Pushing new vars...')
    for site in problem_vars:
        if problem_vars[site]:
            data = {'vars': mistapi.api.v1.sites.setting.getSiteSetting(mist_session, site).data['vars']}
            for var in problem_vars[site]:
                data['vars'][problem_vars[site][var]['New var']['name']] = problem_vars[site][var]['New var']['value']
            # print(json.dumps(data, indent=4))
            response = mistapi.api.v1.sites.setting.updateSiteSettings(mist_session, site, data)
            print(site_names[site] + ' status code: '+str(response.status_code))