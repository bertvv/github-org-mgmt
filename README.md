# Github mgmt

A Python script that creates teams in an organisation, gives each team a
repository with the same name as the team, and adds members. Teams to be created and members are read from a CSV file.

## Prerequisites

The script uses the [PyGithub](http://jacquev6.net/PyGithub/v1/introduction.html) library to use the Github API v3.

## Usage

First, create a configuration file called `config`. See [config.example](config.example) for an example. Copy it over and adapt to your own situation. The configuration should be in JSON format and contains a.o. user credentials. For this reason, the `config` file will be ignored by Git.

Next, create a CSV file `users.csv` (currently still hard coded) with two columns containing team names and login names of members. The file should have a header row containing "login" and "team". Order of rows and columns is irrelevant.

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
Fetching users and teams from CSV. This may take a while...
^_^ project1 ^_^
    alice
    charlie
^_^ project2 ^_^
    bob
    dave
```

## Contribute

Feedback is welcome, you can use the issue tracker to submit bugs, ideas, etc. Pull requests are also appreciated.

## License & disclaimer

This code is public domain.

```
THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND THE CONTRIBUTORS "AS IS" AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
