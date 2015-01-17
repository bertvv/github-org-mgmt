#! /usr/bin/python
# coding=utf8
# Delete all teams and their repositories whose names start with the prefix
# specified on the command line.

from github_org import GithubOrganisationManager as OrgMgr
import sys
from sys import argv

# Check whether the number of arguments is exactly 1
num_args = len(argv) - 1

if num_args != 1:
    print "Expected 1 argument (project name prefix), but got %d" % num_args
    sys.exit(2)

# Check whether the name prefix is long enough.
prefix = argv[1]

# Read config, fetch organization
mgr = OrgMgr('config')

# DELETE the teams
mgr.delete_teams_from_org(prefix)
