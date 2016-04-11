<?php
    $file = "./json/alarms.json";
    $fileHandler = fopen($file, 'w');
    $notifications = $_GET["data"];
    fwrite($fileHandler, $notifications);
    fclose($fileHandler);
?>