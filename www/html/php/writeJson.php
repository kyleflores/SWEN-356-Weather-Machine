<?php
    $file = '../json/settings.json';
    $fileHandler = fopen($file, 'a');
    ftruncate($fileHandler,0);
    $notifications = $_POST['json'];
    fwrite($fileHandler, $notifications);
    fclose($fileHandler);
?>
