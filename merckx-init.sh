#!/bin/bash

#
# download DBpedia 2014 dataset and initialize MERCKX data files
#

echo
echo "MERCKX init - Download DBpedia 2014 dataset and initialize MERCKX data files"
echo "WARNING: files are large so each step may take several minutes to complete..."
echo

# DBpedia download root URL
# DOWNLOAD_PATH=http://downloads.dbpedia.org/2015-04/core-i18n
DOWNLOAD_PATH=http://downloads.dbpedia.org/2014

# create data directories
if [ ! -d dbpedia ]; then
	mkdir dbpedia
fi
if [ ! -d data ]; then
	mkdir data
fi

# extract list of entitites using rdf:type 
if [ ! -f dbpedia/instance_types_en.nt.bz2 ]; then
	echo "*** Downloading DBpedia dataset files..."
	echo "--- Downloading dbpedia/instance_types_en.nt.bz2 ..."
	rm -f dbpedia/instance_types_en.*
	rm -f data/*.lst
	wget -q $DOWNLOAD_PATH/en/instance_types_en.nt.bz2 -P dbpedia
fi
if [ ! -f dbpedia/instance_types_en.nt ]; then
	echo "--- Decompressing dbpedia/instance_types_en.nt.bz2 ..."
	bzip2 -dk dbpedia/instance_types_en.nt.bz2
fi

# rdfs:label in multiple languages (en nl fr ...)
for lang in ${@:-en nl fr}
do
	if [ "$lang" = "en" ]
	then
		if [ ! -f dbpedia/labels_en.nt.bz2 ]; then
			echo "--- Downloading dbpedia/labels_en.nt.bz2 ..."
			wget -q $DOWNLOAD_PATH/en/labels_en.nt.bz2 -P dbpedia
		fi	
		if [ ! -f dbpedia/labels_en.nt ]; then
			echo "--- Decompressing dbpedia/labels_en.nt.bz2 ..."
			bzip2 -dk dbpedia/labels_en.nt.bz2
		fi
	else
		if [ ! -f dbpedia/labels_en_uris_$lang.nt.bz2 ]; then
			echo "--- Downloading dbpedia/labels_en_uris_$lang.nt.bz2 ..."
			wget -q $DOWNLOAD_PATH/$lang/labels_en_uris_$lang.nt.bz2 -P dbpedia
		fi	
		if [ ! -f dbpedia/labels_en_uris_$lang.nt ]; then
			echo "--- Decompressing dbpedia/labels_en_uris_$lang.nt.bz2 ..."
			bzip2 -dk dbpedia/labels_en_uris_$lang.nt.bz2
		fi			
	fi
done

# initialize MERCKX data files
python merckx-init.py $@
