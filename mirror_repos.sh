#! /usr/bin/bash
#
# Author: Bert Van Vreckem <bert.vanvreckem@gmail.com>
#
# 

set -o errexit # abort on nonzero exitstatus
set -o nounset # abort on unbound variable

#{{{ Functions

usage() {
cat << _EOF_
Usage: ${0} PATTERN
  Makes a bare clone of all repositories in the organization matching
  PATTERN.
_EOF_
}

#}}}
#{{{ Command line parsing

if [ "$#" -ne "1" ]; then
    echo "Expected 1 argument, got $#" >&2
    usage
    exit 2
fi

#}}}
#{{{ Variables
repo_regex=$1
repos=$(./list_repos.py | grep "${repo_regex}")
local_dir="${HOME}/prj_repos"
#}}}

# Script proper

if [ -z "${repos}" ]; then
  echo "No repos found that match the search string"
fi

if [ ! -d "${local_dir}" ]; then
  mkdir -p "${local_dir}"
fi

cd "${local_dir}"

for repo in ${repos}; do
  git clone --bare "git@github.com:HoGentTIN/${repo}.git"
done

