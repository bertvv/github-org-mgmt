#! /usr/bin/bash
#
# Author: Bert Van Vreckem <bert.vanvreckem@gmail.com>
#
# 

set -o errexit # abort on nonzero exitstatus
set -o nounset # abort on unbound variable

#{{{ Variables
org=HoGentTIN
source_repo=sjabloon
dest_repo_prefix=ops-g-
from=01
to=11

#vpp_name=testRepo
#}}}

#{{{ Functions

# Rename the VPP project file in the UML branch
rename_vpp() {
  git clone "git@github.com:${org}/${1}.git" temp_repo
  cd temp_repo
  git checkout uml
  git mv "${vpp_name}.vpp" "${1}.vpp"
  git commit --message "VPP-bestand hernoemd naar projectgroep"
  git push
  cd ..
  rm -rf temp_repo
}

#}}}


# Script proper
# Source: https://help.github.com/articles/duplicating-a-repository/

# Create a clone as a ‘bare’ repository (contains *everything*)
git clone --bare "git@github.com:${org}/${source_repo}.git"
cd "${source_repo}.git"

# Push the bare repository back to Github under the new name
for i in $(seq -f "%02g" ${from} ${to}); do
  git push --mirror "git@github.com:${org}/${dest_repo_prefix}${i}.git"
done
cd ..
rm -rf "${source_repo}.git"

# For every repository, perform the VPP name change
#for i in $(seq -f "%02g" ${from} ${to}); do
#  rename_vpp "${dest_repo_prefix}${i}"
#done

