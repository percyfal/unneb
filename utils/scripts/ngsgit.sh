#! /bin/sh
#
# File: ngsgit.sh
# Created: Thu Jul 14 16:37:08 2011
# $Id: $
#
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
# Description:
# Initialize a ngs project repository

usage()
{
    cat <<EOF
Usage: ngsgit.sh repository_name [-w work_dir]

A directory "repository_name" will be created in work_dir (defaulting to ./) and 
the corresponding origin repository will be created in $HOME/private/git/

EOF
}


work_dir=`pwd`
gitbase=/bubo/home/h1/perun/private/git

while getopts ":w:" opt; do
    case $opt in
	w)
	    work_dir=`echo $OPTARG | sed 's/\/$//'`
	    shift
	    shift
	    ;;
	\?)
	    echo "Invalid option: -$OPTARG" >&2
	    exit 1
	    ;;
	:)
	    echo "Option -$OPTARG requires an argument." >&2
	    exit 1
	    ;;
    esac
done

if [[ `echo $work_dir | grep "^/"` ]]; then
    work_dir=$work_dir
else
    work_dir=./$work_dir
fi

if [[ $# -ne 1 ]]; then 
    usage
    exit 1
fi

repository=$1

if [ -d $work_dir/$repository ]; then
    echo $work_dir/$repository exists; not making directory anything
else 
    echo Creating $work_dir/$repository
    mkdir $work_dir/$repository
fi

cd $gitbase
if [ -d $gitbase/$repository ]; then
    echo $gitbase/$repository exists - not doing anything
    exit 1
else 
    echo Creating $gitbase/$repository
    mkdir $gitbase/$repository
    cd $gitbase/$repository
    git init --bare
fi

cd $work_dir/$repository
git init
git remote add origin ssh://perun@biologin.uppmax.uu.se$gitbase/$repository

