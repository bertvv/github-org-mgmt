# A few scripts for managing a Github organization

I use Github for setting up repositories for students working on a programming or system engineering project. We have lots of students (hundreds), typically working in groups of four. That means that creating repositories and assigning users to them manually is not feasible. So I created these scripts to automate the process of setting up (and tearing down) repositories for our students.

## Prerequisites

The script needs the [PyGithub](http://jacquev6.net/PyGithub/v1/introduction.html) library to use the Github API v3.

## Creating repositories and adding users

First, create a configuration file called `ghorg.conf`. See [ghorg.conf.example](ghorg.conf.example) for an example. Copy it over and adapt to your own situation. The configuration should be in JSON format and contains a.o. user credentials. For this reason, all files with extension `.conf` will be ignored by Git.

Next, create a CSV file with two columns containing team names and login names of members. The file should have a header row containing "login" and "team". Order of rows and columns is irrelevant.

```csv
login,team
bob,project2
alice,project1
dave,project2
charlie,project1
```

Then, run the script:

```ShellSession
$ ./create_teams.py users.csv
Fetching users and teams from users.csv. This may take a while...
^_^ project1 ^_^
    alice
    charlie
^_^ project2 ^_^
    bob
    dave
```

## Initializing repositories

You can specify in the configuration to initialize new repositories with a
`README.md` and a `.gitignore`. However, if you already want to add some code,
files, etc., use the `duplicate_repo.sh` script.

Currently, the script doesn't accept command line arguments, so you will need
to edit it in order to use it in your situation. For example:

```Bash
org=myorganization
source_repo=template-repo
dest_repo_prefix=project
from=5
to=20
```

These settings would duplicate repository `template-repo` from organization
`myorganization` into new repositories, named `project05`, `project06`, ...,
`project20`.

A few assumptions:

* The target repositories exist (e.g. created by `create_teams.py`) and are
    completely empty (config file has `auto_init` set to `false`).
* You have the necessary access rights to all repositories
* Target repository names adhere to naming policy `prefixNN` with `prefix` the
    first part of the name that is common to all repos, and `NN` a number
    consisting of exactly two digits (i.e. from `01` to `99`).

## Delete teams and their repository

When preparing for the next semester, it may be necessary to delete all repositories from the previous one. The `delete_teams.py` script will delete all teams with a name starting with a specified prefix from the organization, including any repository with the same name.

**!!! WARNING !!! This is a destructive operation that cannot be undone! See disclaimer below.**

```ShellSession
$ ./delete_teams.py p1g
================================================================================
!!! WARNING WARNING WARNING !!!
This deletes all teams starting with prefix p1g
and their repositories from the organization.
!!! THIS CANNOT BE UNDONE !!!
================================================================================
Teams to be deleted:
p1g01 p1g02 p1g03 p1g04 p1g05 p1g06 p1g07 p1g08 p1g09 p1g10 p1g11 p1g12 p1g13 p1g14 p1g15 
================================================================================
Type in the prefix again to confirm: 
p1g
Deleting p1g01
Deleting p1g02
[...]
Deleting p1g15

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
