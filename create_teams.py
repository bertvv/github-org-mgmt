#! /usr/bin/python
# coding=utf8

from github_org import GithubOrganisationManager as OrgMgr

mgr = OrgMgr('config')

print "Fetching users and teams from CSV. This may take a while..."
teams = mgr.read_teams_from_csv('users.csv')

print "Adding teams to organisation"
mgr.add_teams_to_org(teams)
