# coding=utf8
#

import yaml
import csv
import github
from github import Github
from github import GithubException
from github import UnknownObjectException


class GithubOrganizationManager:
    __slots__ = []
    MIN_PREFIX_LENGTH = 3

    def __init__(self, organization_name):
        self._organization_name = organization_name
        self._config = self.read_config()
        self._github = Github(self._config['user'], self._config['password'])
        self._organization = \
            self._github.get_organization(self._config['organization'])

    def repo_names(self):
        names = self._config['repos']
        if len(names) == 0:
            names.append('')
        return names

    def read_members_from_txt(self, txtfile):
        """Read member names from the specified text file (one member
        per line). An array is returned with NamedUSer objects."""

        user_names = []
        users = []
        failed_users = []
        with open(txtfile) as userfile:
            user_names = userfile.readlines()
        print "Reading users:"
        for name in user_names:
            # strip the \n from the right
            name = name.rstrip()
            print " - %s" % name
            # Convert user name into Github NamedUser object
            try:
                user = self._github.get_user(name)
                users.append(user)
            except UnknownObjectException:
                failed_users.append(name)

        print "Failed users:"
        for failed_user in failed_users:
            print " - %s" % failed_user

        return users

    def read_teams_from_csv(self, csvfile):
        """Read all teams and their users from the specified CSV file.
        A dictionary is returned with team names as key and a list of the team
        members (NamedUser objects) as values e.g.

        {'prj1': [alice, dan], 'prj2': [bob, cathy]}

        If a member does not exist, an exception is raised and the program
        aborts.
        """

        with open(csvfile) as userfile:
            userlist = csv.reader(userfile, delimiter=',')
            header = next(userlist, None)

            assert header.index('login') >= 0, \
                "CSV header should have a login field: %s" % header
            assert header.index('team') >= 0, \
                "CSV header should have a team field: %s" % header

            teams = {}

            for row in userlist:
                team_name = row[header.index('team')]
                login = row[header.index('login')]
                try:
                    user = self._github.get_user(login)

                    if(team_name not in teams):
                        # Add a new key to the teams dict, and
                        # add the first user to the member list
                        teams[team_name] = [user]
                    else:
                        # Append user name to existing team member list
                        teams[team_name].append(user)
                except GithubException:
                    print "%s,%s" % (login, team_name)

        return teams

    def read_config(self):
        """Read the configuration for this organization.
        The file should be in Yaml format. See ‘org-conf.yml.example’.
        """
        config_file_name = self._organization_name + "-conf.yml"
        try:
            with open(config_file_name) as config_file:
                config = yaml.load(config_file)
                return config
        except IOError:
            print("Couldn't load configuration file ‘%s’. "
                  "Maybe you should create it?\n"
                  "See e.g. org-conf.yml.example") % config_file_name
            raise SystemExit

    def invite(self, users):
        """
        Invite the specified users to the organization
        :param str user: Name of a user to invite
        """
        for user_name in users:
            try:
                user = self._github.get_user(user_name)
                if not self._organization.has_in_members(user):
                    print "%s\t\t1\t\t\tuitgenodigd" % user_name
                    self.add_member_to_org(user)
                else:
                    print "%s\t\t\t1\t\treeds lid" % user_name
            except GithubException:
                print "%s\t1\t\t\t\tgebruiker niet gevonden" % user_name

    def add_members_to_team(self, team, user_names):
        """
        Add the specified users to the specified team

        :param team: :class:`github.Team`
        :param user_names: list of str
        :rtype: None
        """

        for user_name in user_names:
            try:
                user = self._github.get_user(user_name)
                self.add_member_to_team(team, user)
            except GithubException:
                print "%s\tgebruiker niet gevonden" % user_name

    def add_member_to_org(self, member):
        """
        Adds the specified NamedUser to the organization
        :calls: `PUT /orgs/:org/memberships/:user
                  <http://developer.github.com/v3/orgs/members>`_
        :param member: :class:`github.NamedUser.NamedUser`
        :rtype: None
        """

        assert isinstance(member, github.NamedUser.NamedUser), member
        url_parameters = {
            "role": "member",
        }
        headers, data = self._organization._requester.requestJsonAndCheck(
            "PUT",
            self._organization.url + "/memberships/" + member._identity,
            parameters=url_parameters
        )

    def add_teams_to_org(self, teams):
        """Adds the specified teams to the organization, including team
        members"""
        repo_config = self._config['repo_config']

        for team_name in sorted(teams.keys()):
            print "- team: %s\n  repos:" % team_name
            team = self._organization.create_team(team_name)
            team.edit(team_name, permission=self._config['repo_access'])

            for rname in self.repo_names():
                repo_name = team_name + rname
                print "    - %s" % repo_name
                repo = self._organization.create_repo(repo_name, **repo_config)
                team.add_to_repos(repo)

            print "  users:"
            self.add_members_to_team(team, teams[team_name])

    def add_member_to_team(self, team, member):
        """
        Adds the specified member, a NamedUser, to the team
        """
        if team.has_in_members(member):
            print "%s\thad al toegang" % member.login
        elif not self._organization.has_in_members(member):
            self.add_member_to_org(member)
            print "%s\tuitgenodigd" % member.login
        else:
            print "%s\ttoegang gegeven" % member.login
            team.add_to_members(member)

    def get_teams_starting_with(self, prefix):
        teams = []
        for team in self._organization.get_teams():
            if team.name.startswith(prefix):
                teams.append(team)
        return teams

    def get_team_by_name(self, team_name):
        for team in self._organization.get_teams():
            if team.name == team_name:
                return team
        raise Exception("Team %s not found" % team_name)

    def get_repos_starting_with(self, prefix):
        repos = []
        for repo in self._organization.get_repos():
            if repo.name.startswith(prefix):
                repos.append(repo)
        return repos

    def delete_repo(self, repo_name):
        """Delete the repository with the specified name from the organization.
        If the repository does not exist, a warning is printed"""

        try:
            print "Deleting repo: %s" % repo_name
            repo = self._organization.get_repo(repo_name)
            repo.delete()
        except GithubException:
            print u"    Repo ‘%s’ already gone. Ignoring..." % repo_name

    def delete_repos(self, repos_to_delete):
        """Delete specified repos. THIS CANNOT BE UNDONE!"""

        print "Deleting repos"
        for repo in repos_to_delete:
            print "- %s" % repo.name
            repo.delete()

    def delete_repos_in_file(self, txtfile):
        """Delete the repos enumerated in the specified text file (one per line).
        THIS CANNOT BE UNDONE!"""

        with open(txtfile) as repofile:
            repos_to_delete = repofile.readlines()
        repos_to_delete = [repo_name.strip() for repo_name in repos_to_delete]

        print '=' * 80
        print '!!! WARNING WARNING WARNING !!!'
        print "This deletes all repos enumerated in file %s" % txtfile
        print '!!! THIS CANNOT BE UNDONE !!!'
        print '-' * 80
        print 'Repos to be deleted:'
        print ', '.join([repo_name for repo_name in repos_to_delete])
        print '=' * 80
        print 'Are you sure you want to do this? [yes/NO]'

        choice = raw_input().lower()

        if choice != 'yes':
            print 'Confirmation failed, bailing out.'
            print u'  Remark: Type ‘yes’ to confirm, not ‘y’'
            return

        for repo_name in repos_to_delete:
            self.delete_repo(repo_name)

    def delete_team(self, team_name):
        """Delete the team with the specified name from the organization.
        If the team does not exist, a warning is printed"""

        try:
            print "Deleting team: %s" % team_name
            team = self._organization.get_team(int(team_name))
            team.delete()
        except GithubException:
            print u"    team ‘%s’ already gone. Ignoring..." % team_name

    def delete_teams_in_file(self, txtfile):
        """Delete the teams enumerated in the specified text file (one per line).
        THIS CANNOT BE UNDONE!"""

        with open(txtfile) as teamfile:
            teams_to_delete = teamfile.readlines()
        teams_to_delete = [team_name.strip() for team_name in teams_to_delete]

        print '=' * 80
        print '!!! WARNING WARNING WARNING !!!'
        print "This deletes all teams enumerated in file %s" % txtfile
        print '!!! THIS CANNOT BE UNDONE !!!'
        print '-' * 80
        print 'Teams to be deleted:'
        print ', '.join([team_name for team_name in teams_to_delete])
        print '=' * 80
        print 'Are you sure you want to do this? [yes/NO]'

        choice = raw_input().lower()

        if choice != 'yes':
            print 'Confirmation failed, bailing out.'
            print u'  Remark: Type ‘yes’ to confirm, not ‘y’'
            return

        for team_name in teams_to_delete:
            self.delete_team(team_name)

    def delete_teams(self, teams_to_delete):
        """Delete specified teams. THIS CANNOT BE UNDONE!"""

        print "Deleting teams"
        for team in teams_to_delete:
                print "- %s" % team.name
                team.delete()

    def delete_teams_and_repos(self, prefix):
        """Delete all teams whose name starts with the specified prefix from
        the organization. This also deletes any repository starting with the
        team name, if it exists. THIS CANNOT BE UNDONE!"""

        assert len(prefix) >= self.MIN_PREFIX_LENGTH, \
            ("Team name prefix is too short. may be deleted. Please use a "
             "prefix of at least %s characters") \
            % self.MIN_PREFIX_LENGTH

        teams_to_delete = self.get_teams_starting_with(prefix)
        repos_to_delete = self.get_repos_starting_with(prefix)

        if len(teams_to_delete) == 0 and len(repos_to_delete) == 0:
            print "No teams or repos start with %s, bailing out" % prefix
            return

        print '=' * 80
        print '!!! WARNING WARNING WARNING !!!'
        print "This deletes all teams starting with prefix %s" % prefix
        print 'and their repositories from the organization.'
        print '!!! THIS CANNOT BE UNDONE !!!'
        print '=' * 80
        print 'Teams to be deleted:'
        print ', '.join([team.name for team in teams_to_delete])
        print '-' * 80
        print 'Repos to be deleted:'
        print ', '.join([repo.name for repo in repos_to_delete])
        print '=' * 80
        print 'Type in the prefix again to confirm: '

        choice = raw_input().lower()

        if choice != prefix.lower():
            print 'Confirmation failed, bailing out.'
            return

        self.delete_teams(teams_to_delete)
        self.delete_repos(repos_to_delete)

    def export_repos_and_contributors(self, prefix):
        """Export repos starting with the specfied prefix and contributors in
        CSV format"""
        repos = self.get_repos_starting_with(prefix)
        print u'repository,login,name,email'
        for repo in repos:
            contributors = repo.get_contributors()
            for contributor in contributors:
                print u'{0},{1},{2},{3}'.format(
                        repo.name,
                        contributor.login,
                        contributor.name,
                        contributor.email)
