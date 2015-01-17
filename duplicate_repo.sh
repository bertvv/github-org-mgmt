#! /usr/bin/bash
#
# Author: Bert Van Vreckem <bert.vanvreckem@gmail.com>
#
# 

set -o errexit # abort on nonzero exitstatus
set -o nounset # abort on unbound variable

#{{{ Variables
org=HoGentTIProjecten1
source_repo=testrepo
dest_repo_prefix=p1g
from=20
to=20
#}}}

# Script proper
# Source: https://help.github.com/articles/duplicating-a-repository/
echo git clone --bare "git@github.com:${org}/${source_repo}.git"
cd "${source_repo}.git"

for i in $(seq -f "%02g" ${from} ${to}); do
  echo git push --mirror "git@github.com:${org}/${dest_repo_prefix}${i}.git"
done
cd ..
rm -rf "${source_repo}.git"
