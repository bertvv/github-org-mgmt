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
Usage: ${0} 

_EOF_
}

#}}}
#{{{ Variables
repo_regex='ops-a'
repos=$(./list_repos.py | grep "${repo_regex}")
local_dir="${HOME}/prj_repos"
#}}}

# Script proper

if [ ! -d "${local_dir}" ]; then
  mkdir -p "${local_dir}"
fi

cd "${local_dir}"

for repo in ${repos}; do
  git clone "git@github.com:HoGentTIN/${repo}.git"
done

