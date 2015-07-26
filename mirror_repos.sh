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
repo_regex='p1g'
repos=$(./list_repos.py -c project1.conf | grep "${repo_regex}")
local_dir="${HOME}/prj_repos"
org=HoGentTIProjecten1
#}}}

# Script proper

if [ ! -d "${local_dir}" ]; then
  mkdir -p "${local_dir}"
fi

cd "${local_dir}"

for repo in ${repos}; do
  git clone "git@github.com:${org}/${repo}.git"
  pushd "${repo}"
  for branch in  $(git branch -a | grep remotes | grep -v HEAD | grep -v master); do
    git branch --track "${branch##*/}" "${branch}"
  done
  git fetch --all
  popd
done

