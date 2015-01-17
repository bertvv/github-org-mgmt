#! /usr/bin/bash
#
# Author: Bert Van Vreckem <bert.vanvreckem@gmail.com>
#
# 

set -o errexit # abort on nonzero exitstatus
set -o nounset # abort on unbound variable

#{{{ Functions

#usage() {
#cat << _EOF_
#Usage: ${0} 

#_EOF_
#}

##}}}
##{{{ Command line parsing

#if [ "$#" -ne "1" ]; then
    #echo "Expected 1 argument, got $#" >&2
    #usage
    #exit 2
#fi

#}}}
#{{{ Variables
org=HoGentTIProjecten1
source_repo=testrepo
dest_repo=p1g20
#}}}

# Script proper
git clone --bare "git@github.com:${org}/${source_repo}.git"

cd "${source_repo}.git"

git push --mirror "git@github.com:${org}/${dest_repo}.git"

cd ..

rm -rf "${source_repo}.git"
