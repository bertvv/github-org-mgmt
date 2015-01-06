# Github mgmt

A Python script that creates teams in an organisation, gives each team a
repository with the same name as the team, and adds members.

## Prerequisites

The script uses the [PyGithub](http://jacquev6.net/PyGithub/v1/introduction.html) library to use the Github API v3.

## Usage

First, create a configuration file called `config`. See [config.example](config.example) for an example. The configuration should be in JSON format and contains a.o. user credentials. For this reason, the `config` file will be ignored by Git.

Next, create a CSV file `users.csv` (currently still hard coded) with two columns containing team names and login names of members. Order of rows and columns is irrelevant.

```csv
login,team
bob,project2
alice,project1
dave,project2
charlie,project1
```

Then, run the script:

```
$ python create_teams.py
```
