#!/usr/bin/python

'''
Write the test or current version to a file on the computer

The idea is that we write the test version from AutoPkg into an EA.
When the EA runs, it writes the test version from the EA into the file.

When we stage a policy, we write the current version to the same EA.
When the EA runs, it writes the current version from the EA into the file.

We need to write to a file, because when AutoPkg uploads the EA, it will not
have the current version in it, as it will overwrite the existing EA.

The policy stager will need to grab the EA using the API and edit it and
re-upload it.
'''

import os
import json


# print "\n{0} test version: {1}\n".format(policy_name, test_version)

def write_to_json(policy_name, version_check_type, app_path, app_key, pkgid, version, version_type, script_version=None):
    # check that path exists
    version_file_location = '/Library/Application Support/JAMF'
    version_file = 'software_versions.json'

    if not os.path.exists(version_file_location):
        print "Creating directory {}".format(version_file_location)
        os.mkdir(version_file_location)

    # check that file exists
    version_filepath = os.path.join(version_file_location, version_file)
    try:
        f = open(version_filepath, 'r')
        try:
            print "{} exists, will amend".format(version_file)
            info = json.load(f)
        except ValueError:
            print "{} is empty, will overwrite".format(version_file)
            info = {}
        f.close()
    except IOError:
        print "{} doesn't yet exist, will create".format(version_file)
        info = {}

    policy_match = False

    # check if the policy already has an entry
    for key, value in info.iteritems():
        # print key, value
        if key == policy_name:
            # marker to show that policy has an entry
            policy_match = True
            # change version to match the new value
            if version_type == 'untested':
                value['jamf_test_version'] = version
            elif version_type == 'current':
                value['jamf_current_version'] = version
            value['version_check_type'] = version_check_type
            value['app_path'] = app_path
            value['app_key'] = app_key
            value['pkgid'] = pkgid
            value['script_version'] = script_version

    # if there's no entry for this policy, append it
    # note we should never be writing a current version to an empty value
    # as the untested policy should always get there before the staged policy
    if policy_match == False and version_type == 'untested':
        info[policy_name] = {
                            'jamf_test_version': version,
                            'version_check_type': version_check_type,
                            'app_path': app_path,
                            'app_key': app_key,
                            'pkgid': pkgid,
                            'script_version': script_version
                            }

    # print the output - for test purposes only
    print "\nOutput:"
    print json.dumps(info, sort_keys=True, indent=4)

    f = open(version_filepath, 'w+')
    # write (back) to file
    json.dump(info, f, indent=4)
    f.close()
