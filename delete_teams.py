#! /usr/bin/python
# coding=utf8
# Delete all teams and their repositories whose names start with the prefix
# specified on the command line.

from github import Github
import github_org as org
import sys
from sys import argv

MIN_PREFIX_LENGTH = 3

# Check whether the number of arguments is exactly 1
num_args = len(argv) - 1

if num_args != 1:
    print "Expected 1 argument (project name prefix), but got %d" % num_args
    sys.exit(2)


# Check whether the name prefix is long enough.
prefix = argv[1]

if len(prefix) < MIN_PREFIX_LENGTH:
    print "Team name prefix is very short. This implies that a lot of teams"
    print "may be deleted. Please use a prefix of at least %s characters" \
        % MIN_PREFIX_LENGTH
    sys.exit(1)

# Read config, fetch organization
config = org.read_config()
github = Github(config['user'], config['password'])
organisation = github.get_organization(config['organisation'])

# DELETE the suckers
org.delete_teams_from_org(organisation, prefix)
