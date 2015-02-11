#! /usr/bin/python
# coding=utf8

import sys
from github_org import GithubOrganizationManager as OrgMgr
from getopt import getopt, GetoptError

#
# Helper functions
#


def usage():
    print ("Usage: %s [OPTION]... [USERS_CSV]\n"
           "  -h  --help         Print this help message and exit\n"
           "  -c  --config=FILE  Read configuration from the specified file"
           "\n") % sys.argv[0]

#
# Parse command line
#
config_file = 'ghorg.conf'
user_file = 'users.csv'

try:
    opts, args = getopt(sys.argv[1:],
                        "hc:",
                        ['help', 'config='])
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

if len(args) > 0:
    user_file = args[0]

#
# Script proper
#

mgr = OrgMgr(config_file)

print "Fetching users and teams from %s. This may take a while..." \
    % user_file
print "Failed users (if any):"
teams = mgr.read_teams_from_csv(user_file)

print "Adding teams to organization"
mgr.add_teams_to_org(teams)
