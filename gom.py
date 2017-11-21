#! /usr/bin/python
# coding=utf8
# gom.py -- Command line tool for managing a Github organization

import sys
from github_org import GithubOrganizationManager as OrgMgr

#
# Helper functions
#


def usage():
    print"""
Usage %s ORGANIZATION ACTION [OPTION]...

ORGANIZATION is the name of the Github organization to be managed. You should
  have a configuration file named 'ORGANIZATION-conf.yml' in the working
  directory.

ACTIONS

  c, create-teams CSV     creates teams and members from the specified CSV file
  p, purge-teams PREFIX   delete all teams and associated repos that have a
                          name starting with PREFIX
     delete-teams TXT     deletes all teams enumerated in the specified TXT file
     delete-repos TXT     deletes all repos enumerated in the specified TXT file
  l, list-repos           prints all repositories in the organization
  x, export-teams PREFIX  export repositories starting with PREFIX and members
                          as a CSV file

"""[1:-1] % sys.argv[0]


def list_repos(manager):
    """List repositories in the organization."""
    repos = manager._organization.get_repos()
    for repo in repos:
        print repo.name

def list_teams(manager):
    """List teams in the organization."""
    teams = manager._organization.get_teams()
    for team in teams:
        print team.name

def delete_repos(manager, options):
    """Delete repositories enumerated in the specified text file"""
    if len(options) < 1:
        print "No file containing repo names specified!"
        usage()
        sys.exit(1)

    manager.delete_repos_in_file(options[0])

def delete_teams(manager, options):
    """Delete teams enumerated in the specified text file"""
    if len(options) < 1:
        print "No file containing team names specified!"
        usage()
        sys.exit(1)

    manager.delete_teams_in_file(options[0])

def create_teams(manager, options):
    """Create new teams and repositories"""
    if len(options) < 1:
        print "No user file specified!"
        usage()
        sys.exit(1)

    user_file = options[0]

    print "Fetching users and teams from %s. This may take a while." \
        % user_file
    print "Failed users (if any):"
    teams = manager.read_teams_from_csv(user_file)

    print "Adding teams to organization"
    manager.add_teams_to_org(teams)


def purge_teams(manager, options):
    """Delete teams and their repos starting with the specified prefix"""
    if len(options) < 1:
        print "No name prefix of teams to delete specified!"
        usage()
        sys.exit(1)

    prefix = options[0]

    manager.delete_teams_and_repos(prefix)


def export_repos(manager, options):
    """Export repos starting with the specified prefix and their contributors as a CSV file"""
    if len(options) < 1:
        print "No name prefix of teams to export specified!"
        usage()
        sys.exit(1)
    prefix = options[0]
    manager.export_repos_and_contributors(prefix)


def add_members_to_team(manager, options):
    """Adds members from a text file to a team"""
    if len(options) < 2:
        print "No team/member list specified!"
        usage
        sys.exit(1)
    team_name = options[0]
    user_file = options[1]
    print "Fetching users from %s." % user_file
    users = manager.read_members_from_txt(user_file)
    manager.add_members_to_team(team, users)

#
# Script proper
#

if len(sys.argv) < 3:
    print "Not enough arguments, expected at least 2"
    usage()
    sys.exit(2)

organization_name = sys.argv[1]
action = sys.argv[2]
options = sys.argv[3:]
manager = OrgMgr(organization_name)

# print "Org    : %s" % manager._organization_name
# print "Action : %s" % action
# print "Options: %s" % ', '.join(options)

if action == "list-repos" or action == "l":
    list_repos(manager)
if action == "list-teams" or action == "l":
    list_teams(manager)
elif action == "export-teams" or action == "x":
    export_repos(manager, options)
elif action == "create-teams" or action == "c":
    create_teams(manager, options)
elif action == "delete-repos":
    delete_repos(manager, options)
elif action == "purge-teams" or action == "p":
    purge_teams(manager, options)
elif action == "delete-teams" or action == "d":
    delete_teams(manager, options)
elif action == "add-members" or action == "a":
    add_members_to_team(manager, options)
else:
    print "Unknown action: %s" % action
    usage()
    sys.exit(1)
