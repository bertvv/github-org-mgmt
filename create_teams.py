#! /usr/bin/python
# coding=utf8

from github import Github
import github_org as org

config = org.read_config()
github = Github(config['user'], config['password'])
organisation = github.get_organization(config['organisation'])

print "Fetching users and teams from CSV. This may take a while..."
teams = org.read_teams_from_csv(github)
org.add_teams_to_org(organisation, teams, config)


# WARNING!!! This deletes all teams starting with 'p1g' from the organisation
# THIS CANNOT BE UNDONE, so leave in comment unless you really want this.
# delete_teams_from_org(organisation, 'p1g')
