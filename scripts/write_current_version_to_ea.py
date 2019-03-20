#!/usr/bin/python

'''
Writes the current version number to the relevant Extension Attributes.
For use during staging a policy to production.
'''

import sys
import jss

jss_prefs = jss.JSSPrefs()
j = jss.JSS(jss_prefs)


def write_version_to_ea(policy_name, version):
    """Grabs the EA from the server, overwrites the current version, then writes it back"""
    ea_name = '{} Version'.format(policy_name)

    data = j.ComputerExtensionAttribute(ea_name)
    ea_content = data.findtext('input_type/script')

    change_made = False
    line_should_be = 'jamf_current_version = "{}"'.format(version)
    replacement_ea_content = ''
    for line in ea_content.splitlines():
        if 'jamf_current_version =' in line and line != line_should_be:
            line = line_should_be
            change_made = True
        replacement_ea_content = replacement_ea_content + line + '\n'
    # reconstruct the XML and write it back if it changed
    if change_made:
        data.find('input_type/script').text = replacement_ea_content
        data.save()

    data = j.ComputerExtensionAttribute(ea_name)
    ea_content = data.findtext('input_type/script')
    print ea_content

def main():
    """insert policy name and version from command line"""
    policy_name = sys.argv[1]
    version = sys.argv[2]
    write_version_to_ea(policy_name, version)


if __name__ == '__main__':
    main()
