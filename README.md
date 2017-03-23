# MERCKX
Code source of MERCKX (Multilingual Entity/Resource Combiner & Knowledge eXtractor) and related material for the Historische Kranten project (http://historischekranten.be)

Demo available at http://mastic.ulb.ac.be/ypres/

## Usage

Run `./merckx-init.sh` to download all resources from DBpedia.

Then use `merckx.py <type> <filename>` where `<type>` is the entity type (EVE, LOC, PER, or ORG) and `<filename>` is the name of text file to analyze.