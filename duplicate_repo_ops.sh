#! /usr/bin/bash
#
# Author: Bert Van Vreckem <bert.vanvreckem@gmail.com>
#
# 

set -o nounset # abort on unbound variable

#{{{ Variables
org=HoGentTIN
source_repo=sjabloon
dest_repo_prefix=ops3-g
from=01
to=08

#vpp_name=testRepo
#}}}

#{{{ Functions

#}}}


# Script proper
# Source: https://help.github.com/articles/duplicating-a-repository/

# Create a clone as a ‘bare’ repository (contains *everything*)
git clone --bare "git@github.com:${org}/${source_repo}.git"
cd "${source_repo}.git"

# Push the bare repository back to Github under the new name
for i in $(seq -f "%02g" ${from} ${to}); do
  echo "Pushing to: git@github.com:${org}/${dest_repo_prefix}${i}.git"
  git push --mirror "git@github.com:${org}/${dest_repo_prefix}${i}.git"
done
cd ..
rm -rf "${source_repo}.git"


