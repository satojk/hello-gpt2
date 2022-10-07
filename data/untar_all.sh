#!/bin/bash

# Assumes openwebtext is a directory containing several .xz files. This is the 
# case if you have just downloaded openwebtext.tar.xz and then run tar -xf 
# openwebtext.tar.xz.

cd openwebtext;

for file in $(ls); do
  if [[ $file == *.xz ]]; then
    mkdir "${file%.*}";
    mv $file ${file%.*};
    cd ${file%.*};
    tar -xvf $file;
    cd ..;
  fi
done;

cd ..
