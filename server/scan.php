<?php
$key = $_GET['key'] ?? '';
if ($key !== 'wifi123456') die('invalid key');

$list = shell_exec('/usr/local/bin/wifi-scan.sh');
echo $list;
?>
