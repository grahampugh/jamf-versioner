#!/usr/bin/python

'''
Use Munki's core tools to
compare the installed version of an application
with the last version installed by Jamf
'''

import sys
import os
import httplib
import base64
import json

munkitools_path = '/usr/local/munki'
sys.path.append(munkitools_path)
from munkilib import pkgutils
# from munkilib import FoundationPlist


def compare_versions(local, jamf, version):
    '''compare local version to jamf versions stored in
    json file. Returns one of:
    -current or -untested
    =current or =untested
    +current or +untested
    '''
    latest = '+{}'.format(version)
    highest_version = local
    if (pkgutils.MunkiLooseVersion(highest_version) ==
            pkgutils.MunkiLooseVersion(jamf)):
        latest = '={}'.format(version)
    elif (pkgutils.MunkiLooseVersion(highest_version) <
            pkgutils.MunkiLooseVersion(jamf)):
        latest = '-{}'.format(version)
        highest_version = jamf
    return latest, highest_version


def ext_att_output(policy_name):
    '''supplies values to compare local versions with current and untested
    versions on Jamf. Returns a composite EA value'''

    # grab information from json file
    # check that path exists
    version_file_location = '/Library/Application Support/JAMF'
    version_file = 'software_versions.json'

    if not os.path.exists(version_file_location):
        return 'No version information'

    # check that file exists
    version_filepath = os.path.join(version_file_location, version_file)
    try:
        f = open(version_filepath, 'r')
        try:
            print "{} exists".format(version_file)
            info = json.load(f)
            f.close()
        except ValueError:
            return 'No version information'
    except IOError:
        return 'No version information'

    version_check_type = info[policy_name]['version_check_type']
    app_path = info[policy_name]['app_path']
    app_key = info[policy_name]['app_key']
    pkgid = info[policy_name]['pkgid']
    if info[policy_name]['script_version']:
        script_version = info[policy_name]['script_version']
    else:
        script_version = '0'

    # greb the test version
    jamf_test_version = info[policy_name]['jamf_test_version']
    print "jamf_test_version: {}".format(jamf_test_version) # temp

    # check if the current version is written in the EA
    try:
        jamf_current_version = info[policy_name]['jamf_current_version']
        print "jamf_current_version: {}".format(jamf_current_version) # temp
    except KeyError:
        # we set a current version of more than zero but less
        # than any feasible real version number so that we can
        # compare - may need to check if something like R2018
        # appears as less than this
        jamf_current_version = "0.0.0.0.1"

    if version_check_type == "app":
        # get installed app version
        if app_path.endswith('.app') or app_path.endswith('.plugin') or app_path.endswith('/Current'):
            # this function automatically adds Contents/Info.plist to the path
            local_version = pkgutils.getBundleVersion(app_path, app_key)
        if not local_version:
            local_version = "0"
        print "app version: {}".format(local_version) # temp
    elif version_check_type == "pkg":
        # get last version installed from pkg
        local_version = pkgutils.getInstalledPackageVersion(pkgid)
        if not local_version:
            local_version = "0"
        print "pkg version: {}".format(local_version) # temp
    elif version_check_type == "script":
        # the version will be passed from the extension attribute in this case
        local_version = script_version
        if not local_version:
            local_version = "0"
    # compare local with current
    latest_v_current, highest_version = compare_versions(
        local_version, jamf_current_version, 'current'
    )

    # compare local with untested
    latest_v_untested, highest_version = compare_versions(
        local_version, jamf_test_version, 'untested'
    )

    output = "{},{},{}".format(local_version,latest_v_current, latest_v_untested)
    return output
