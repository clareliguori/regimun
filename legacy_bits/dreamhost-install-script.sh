#!/bin/sh

# install python modules
cd django_regimun/python_mods/
for f in *.tar.gz
do
    tar xvfz $f
done

current_dir=`pwd`
versions=("2.4" "2.5" "2.6")
for v in $versions
do
    mkdir -p lib/python$v/site-packages
    export PYTHONPATH=$PYTHONPATH:$current_dir/lib/python$v/site-packages
done

for d in *
do
    if [ -d $d ]; then
	cd $d
	python setup.py install --prefix=..
	cd ..
    fi
done

for v in $versions
do
    if [ -d lib/python$v/site-packages ]; then
	for f in lib/python$v/site-packages/*.egg
	do
	    unzip $f
	done
    fi
done

mkdir tmp
uptime > tmp/restart.txt