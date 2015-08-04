#
# Extract DBpedia places & labels
#

echo "*** Downloading DBpedia instance types..."
rm -f instance_types_en.nt.bz2
wget -q http://downloads.dbpedia.org/2014/en/instance_types_en.nt.bz2

echo "*** Decompressing DBpedia instance types..."
rm -f instance_types_en.nt
bzip2 -dk instance_types_en.nt.bz2

echo "*** Extracting DBpedia places..."
grep "<http://dbpedia.org/ontology/Place>" instance_types_en.nt | awk '{print $1}' | sed 's/^<http:\/\/dbpedia.org\/resource\//dbr:/g' | sed 's/>$//g' | sort -u > dbpedia-places.lst

echo "*** Downloading DBpedia labels..."
# rm -f labels_en.nt.bz2
# wget -q http://downloads.dbpedia.org/2014/en/labels_en.nt.bz2
rm -f labels_en_uris_fr.nt.bz2
wget -q http://downloads.dbpedia.org/2014/fr/labels_en_uris_fr.nt.bz2
rm -f labels_en_uris_nl.nt.bz2
wget -q http://downloads.dbpedia.org/2014/nl/labels_en_uris_nl.nt.bz2

echo "*** Decompressing DBpedia labels..."
# rm -f labels_en.nt
# bzip2 -dk labels_en.nt.bz2
rm -f labels_en_uris_fr.nt
bzip2 -dk labels_en_uris_fr.nt.bz2
rm -f labels_en_uris_nl.nt
bzip2 -dk labels_en_uris_nl.nt.bz2

echo "*** Extracting DBpedia labels..."
python dbpedia-extract.py