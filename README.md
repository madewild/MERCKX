# MERCKX
Code source of MERCKX (Multilingual Entity/Resource Combiner & Knowledge eXtractor) and related material for the Historische Kranten project (http://historischekranten.be)

Demo available at http://mastic.ulb.ac.be/ypres/

## Usage

Warning: requires Python 2.7 (no support planned for Python 3 yet).

Run `./merckx-init.sh` to download all resources from DBpedia. This will automatically call `merckx-init.py` to generate labels and entities.

Then use `merckx.py <type> <filename>` where `<type>` is the entity type (EVE, LOC, PER, or ORG) and `<filename>` is the name of text file to analyze.
For instance, `merckx.py LOC example.txt` (first part of the Wikipedia article about Belgium) will give the following output:

belgium.txt	35	    41	    dbr:Belgium
belgium.txt	72	    80	    dbr:Belgium
belgium.txt	208	    214	    dbr:Europe
belgium.txt	227	    233	    dbr:France
belgium.txt	239	    250	    dbr:Netherlands
belgium.txt	281	    290	    dbr:North_Sea
belgium.txt	506	    512	    dbr:Europe
belgium.txt	847	    856	    dbr:High_Fens
belgium.txt	914	    925	    dbr:Netherlands
belgium.txt	971	    977	    dbr:France
belgium.txt	1181	1195	dbr:Gallia_Belgica
belgium.txt	1429	1440	dbr:Netherlands
belgium.txt	1563	1569	dbr:Europe
belgium.txt	1861	1869	dbr:Flanders
belgium.txt	1926	1934	dbr:Wallonia
belgium.txt	1940	1948	dbr:Brussels
belgium.txt	2029	2043	dbr:Flemish_Region
belgium.txt	2094	2102	dbr:Wallonia
belgium.txt	2695	2703	dbr:Flanders
belgium.txt	2708	2716	dbr:Wallonia
belgium.txt	3299	3313	dbr:European_Union
belgium.txt	3386	3400	dbr:European_Union
belgium.txt	3495	3503	dbr:Brussels
belgium.txt	3633	3641	dbr:Brussels
belgium.txt	3804	3812	dbr:Schengen,_Luxembourg
