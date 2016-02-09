#! /usr/bin/python
# coding=utf8
# Delete all teams and their repositories whose names start with the prefix
# specified on the command line.

from getopt import getopt, GetoptError
from github_org import GithubOrganizationManager as OrgMgr
import sys

#
# Helper functions
#


def usage():
    print ("Usage: %s [OPTION]... [PREFIX]\n"
           "  -h  --help         Print this help message and exit\n"
           "  -c  --config=FILE  Read configuration from the specified file\n"
           "\nWARNING!!! This script will delete repositories from\n"
           "Github. THIS CANNOT BE UNDONE!") % sys.argv[0]

#
# Parse command line
#
config_file = 'ghorg.conf'

try:
    opts, args = getopt(sys.argv[1:], "hc:", ['help', 'config='])
except GetoptError as err:
    print str(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

for opt, opt_arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(0)
    if opt in ('-c', '--config'):
        config_file = opt_arg
    else:
        assert False, "unhandled option: %s" % opt

if len(args) != 1:
    print "Expected 1 argument (project name prefix), but got %d" % len(args)
    sys.exit(2)

# Check whether the name prefix is long enough.
prefix = args[0]

# Read config, fetch organization
mgr = OrgMgr(config_file)

# DELETE the teams
mgr.delete_repos_from_org(prefix)
