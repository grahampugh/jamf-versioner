#!/usr/bin/python

'''
An Extension Attribute that uses Munki's core tools to
compare the installed version of an application
with the last version installed by Jamf
'''
import sys

versioner_path = '/usr/local/munki/versioner'
sys.path.append(versioner_path)
from write_version_to_json_file import write_to_json
from jamf_versioner import ext_att_output

### INPUTS
policy_name = sys.argv[1]
version_check_type = '%VERSIONER_TYPE%' # app or pkg or script
app_path = '%VERSIONER_APP_PATH%'
app_key = sys.argv[2]
pkgid = '%PKGID%'
jamf_test_version = '%version%'
jamf_current_version = '0.0.0'
### END INPUTS


# optional section to determine the version by commands
# such as a non-app like Java
# add an optional 'script_version' key as the last item in the
# write_to_json function

# set defaults if not supplied from AutoPkg
if '%' in version_check_type:
    version_check_type = 'app'
if '%' in app_path:
    app_path = '/Applications/{}.app'.format(policy_name)
if '%' in app_key:
    app_key = 'CFBundleShortVersionString'
if '%' in pkgid:
    pkgid = ''

# write to json_file
jamf_test_version = sys.argv[3] # testing only
jamf_current_version = sys.argv[4] # testing only
write_to_json(policy_name, version_check_type, app_path, app_key, pkgid, jamf_test_version, 'untested')
if jamf_current_version != '0.0.0':
    write_to_json(policy_name, version_check_type, app_path, app_key, pkgid, jamf_current_version, 'current')


# write out EA
output = ext_att_output(policy_name)
print "<result>{}</result>".format(output)
