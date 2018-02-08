<?php
$json = file_get_contents('php://input');
$obj = json_decode($json, true);
$outfile = fopen('/jsegoviamartin.github.io/experiments/'.$obj["filename"], "a");
fwrite(
    $outfile,
    sprintf($obj["filedata"])
);
fclose($outfile);
?>
