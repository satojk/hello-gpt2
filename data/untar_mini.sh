#!/bin/bash

# Assumes ./openwebtext is a directory containing several .xz files. This is 
# the case if you have just downloaded openwebtext.tar.xz and then run tar 
# -xf openwebtext.tar.xz.

# This script will extract shards 101, 301, 501, 701, 901 from each 
# subset. That is, it extracts ~0.5% of OpenWebText, assuming all .xz files are 
# in the ./openwebtext dir. To extract all .xz files in ./openwebtext 
# regardless of number, run untar_all.sh instead.

# WARNING: This script will delete all .xz files, in ./openwebtext, leaving 
# behind only the extracted contents of the ones mentioned above.

cd openwebtext;

for i in 1 3 5 7 9; do
    for file in $(ls); do
      if [[ $file == *-${i}01_data.xz ]]; then
        mkdir "${file%.*}";
        mv $file ${file%.*};
        cd ${file%.*};
        tar -xvf $file;
        rm $file;
        cd ..;
      fi
    done;
done;

rm *.xz;

cd ..
