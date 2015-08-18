<!DOCTYPE html>
<html>

<head>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
<title>People Finder</title>
<style>
img {max-height:200px;max-width:150px}
.pic {text-align:center; float:left; width:170px; height:300px; display: table-cell; vertical-align: bottom;}
td {text-align:center;}
</style>
<script>
function getLoc() {
    document.getElementById("form").submit();
}
</script>
</head>

<body>
<?php
$down = False;
try {
  $test = file_get_contents("http://dbpedia.org/data/Ypres.json");
}
catch(Exception $e) {
  $down = True;
}
if($down) {
echo '<h2>Sorry, DBpedia is down at this time, please try again later...</h2>';
}
elseif(!(isset($_GET["loc"]))) {
  $places = Array("Passendale", "Ypres", "Zonnebeke", "Poperinge", "Diksmuide", "Ostend");
  echo '
  <div align="center">
  <h2>Find people born in these common places:</h2><table><tr>';
  $base = 'http://dbpedia.org/data/';
  foreach($places as $place){
    echo '<td><b>'.$place.'</b><br>';
    $url = $base.$place.'.json';
    $json = file_get_contents($url);
    $res = json_decode($json,true);
    $img = $res["http://dbpedia.org/resource/".$place]["http://dbpedia.org/ontology/thumbnail"][0]["value"];
    echo '<a href="?loc='.$place.'"><img src="'.$img.'"/></a></td>';
  }
  echo '</tr></table><h2>or choose your own place:</h2>
  <form id="form" action="">
  Location: <input type="text" name="loc">
  <input type="button" onclick="getLoc()" value="Submit">
  </form></div>';
}
else {
  $loc = ucwords(strtolower($_GET["loc"]));
  echo '<h2>Some people born in ' . htmlspecialchars($loc) . ':</h2>';
  $base = 'http://dbpedia.org/sparql?';
  $data = array('default-graph-uri'=>'http://dbpedia.org',
	      'query'=>'select distinct ?per ?img where {
  ?per <http://dbpedia.org/ontology/birthPlace> <http://dbpedia.org/resource/'.urlencode(str_replace(" ","_",$loc)).'> .
  ?per <http://dbpedia.org/ontology/thumbnail> ?img
  } LIMIT 30',
              'format'=>'application/sparql-results+json',
	      'timeout'=>30000,
	      'debug'=>'on');
  $url = $base.http_build_query($data);
  $json = file_get_contents($url);
  $res = json_decode($json,true);
  echo '<div>';
  foreach($res["results"]["bindings"] as $key=>$val){
    $uri = $val["per"]["value"];
    $per = urldecode(str_replace("_"," ",substr($uri,28)));
    $img = $val["img"]["value"];
    /*$size = getimagesize($img);
    if(is_array($size)){*/
    $wiki = 'http://en.wikipedia.org/wiki/'.str_replace(" ","_",$per);
    echo '<div class="pic"><b>'.$per.'</b><br>';
    echo '<a href="'.$wiki.'"><img src="'.$img.'"/></a></div> ';
    /*}*/
  }
  echo '</div>';
}
?>

</body>
</html>
