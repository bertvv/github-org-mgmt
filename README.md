# A few scripts for managing a Github organization

I use Github for setting up repositories for students working on a programming or system engineering project. We have lots of students (hundreds), typically working in groups of four. That means that creating repositories and assigning users to them manually is not feasible. So I created these scripts to automate the process of setting up (and tearing down) repositories for our students.

## Prerequisites

The script needs the [PyGithub](http://jacquev6.net/PyGithub/v1/introduction.html) library to use the Github API v3.

```ShellSession
$ pip install PyGithub
```

## Creating repositories and adding users

First, create a configuration file called `ORGANIZATION-conf.yml` (with ORGANIZATION of course the name of your Github organization). See [example-conf.yml](example-conf.yml) for an example. Copy it over and adapt to your own situation. The configuration should be in Yaml format and contains a.o. user credentials. For this reason, all files that end with `-conf.yml` will be ignored by Git.

```Yaml
---
# Organization name
organization: example

# User credentials. WARNING! This contains your password.
# Don't put this under version control!
user: horace
password: letmein

# Sequence of repos to be created for each team. Will be
# prepended with the team name. If you leave this empty,
# each team gets a repository with the team name:
#   repos: []
repos:
  - a
  - b

# Default repository access for team members.
# One of 'pull', 'push', or 'admin'
repo_access: push

# Several settings for creating a repo.
repo_config:
  private: false
  has_issues: true
  has_wiki: true
  has_downloads: true
  auto_init: false
  gitignore_template: ''
```

Next, create a CSV file with two columns containing team names and login names of members. The file should have a header row containing "login" and "team". Order of rows and columns is irrelevant.

```csv
login,team
bob,project2
alice,project1
dave,project2
charlie,project1
```

Then, run the script `gom.py` to create the teams. Running it without options gives a Usage message:

```ShellSession
$ ./gom.py
Not enough arguments, expected at least 2
Usage ./gom.py ORGANIZATION ACTION [OPTION]...

ORGANIZATION is the name of the Github organization to be managed. You should
  have a configuration file named 'ORGANIZATION-conf.yml' in the working
  directory.

ACTIONS

  c, create-teams CSV     creates teams and members from the specified CSV file
  d, delete-teams PREFIX  delete all teams and associated repos that have a
                          name starting with PREFIX
  l, list-repos           prints all repositories in the organization


```

Creating the teams goes like this:

```ShellSession
$ ./gom.py example create-teams example-users.csv
Fetching users and teams from example-users.csv. This may take a while.
Failed users (if any):
Adding teams to organization
- team: project1
  repos:
    - project1a
    - project1b
  users:
    - alice
    - charlie
- team: project2
  repos:
    - project2a
    - project2b
  users:
    - bob
    - dave
```

## Delete teams and their repositories

It is possible to delete multiple teams and repositories from the organization. You specify a prefix and all teams and repositories with a name starting with that prefix will be deleted.

**!!! WARNING !!! This is a destructive operation that cannot be undone! See disclaimer below.**

```ShellSession
$ ./gom.py example delete-teams proj
================================================================================
!!! WARNING WARNING WARNING !!!
This deletes all teams starting with prefix team
and their repositories from the organization.
!!! THIS CANNOT BE UNDONE !!!
================================================================================
Teams to be deleted:
project1, project2
--------------------------------------------------------------------------------
Repos to be deleted:
project1a, project1b, project2a, project2b
================================================================================
Type in the prefix again to confirm: 
proj
Deleting teams
- project1
- project2
Deleting repos
- project1a
- project1b
- project2a
- project2b
```

## Contribute

All feedback is welcome! You can use the issue tracker to submit bugs, ideas, etc. Pull requests are also appreciated.

## License & disclaimer

This code is released under the 2-clause BSD license.

```
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
