# MERCKX

Source code of MERCKX (Multilingual Entity/Resource Combiner & Knowledge eXtractor) and related material for the Historische Kranten project (<http://historischekranten.be>)

Demo available at <http://mastic.ulb.ac.be/ypres/>

## Usage

Run `./merckx-init.sh` to download all resources from DBpedia. This will automatically call `merckx-init.py` to generate labels and entities.

Then use `python3 merckx.py <type> <filename>` where `<type>` is the entity type (EVE, LOC, PER, or ORG) and `<filename>` is the name of text file to analyze.
For instance, `python3 merckx.py LOC example.txt` (first part of the Wikipedia article about Belgium) will give the following output:

```tsv
example.txt     35      41      dbr:Belgium
example.txt     72      80      dbr:Belgium
example.txt     208     214     dbr:Europe
example.txt     227     233     dbr:France
example.txt     239     250     dbr:Netherlands
example.txt     506     512     dbr:Europe
example.txt     847     856     dbr:High_Fens
example.txt     914     925     dbr:Netherlands
example.txt     971     977     dbr:France
example.txt     1429    1440    dbr:Netherlands
example.txt     1563    1569    dbr:Europe
example.txt     1861    1869    dbr:Flanders
example.txt     1926    1934    dbr:Wallonia
example.txt     1940    1948    dbr:Brussels
example.txt     2029    2043    dbr:Flemish_Region
example.txt     2094    2102    dbr:Wallonia
example.txt     2695    2703    dbr:Flanders
example.txt     2708    2716    dbr:Wallonia
example.txt     3495    3503    dbr:Brussels
example.txt     3633    3641    dbr:Brussels
example.txt     3804    3812    dbr:Schengen,_Luxembourg
```
