#! /usr/bin/python
# coding=utf8

from github import Github
import json
import csv


def read_teams_from_csv(csvfile='users.csv'):
    """Read all teams and their users from the specified CSV file.
    A dictionary is returned with team names as key and a list of the team
    member's login names as values e.g.

      {'prj1': ['alice', 'dan'], 'prj2': ['bob', 'cathy']}
    """

    with open('users.csv') as userfile:
        userlist = csv.reader(userfile, delimiter=',')
        header = next(userlist, None)

        assert header.index('login') >= 0, \
            "CSV header should have a login field: %s" % header
        assert header.index('team') >= 0, \
            "CSV header should have a team field: %s" % header

        teams = {}

        for row in userlist:
            login = row[header.index("login")]
            team_name = row[header.index("team")]
            print login, team_name
            if(team_name not in teams):
                teams[team_name] = [login]
            else:
                teams[team_name].append(login)

    return teams


def read_config(config_file_name='config'):
    try:
        with open(config_file_name) as config_file:
            config = json.load(config_file)
            return config
    except IOError:
        print ("Couldn't load configuration file «%s». "
               "Maybe you should create it?\n"
               "See config.example for an example") % config_file_name
        raise SystemExit


# Script proper

config = read_config()
github = Github(config['user'], config['password'])

org = github.get_organization(config['organisation'])

#bert = g.get_user("bertvv")
#print bert
#team = tin.create_team("p1g01")
#repo = tin.create_repo("p1g01",
                       #description="Project 1 groep 1",
                       #private=True,
                       #has_issues=True,
                       #has_wiki=True,
                       #has_downloads=True,
                       #auto_init=True,
                       #gitignore_template="Java")
#team.add_to_repos(repo)
