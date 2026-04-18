<?php
$key = $_GET['key'] ?? '';
$ssid = $_GET['ssid'] ?? '';
$pwd = $_GET['pwd'] ?? '';

if ($key !== 'wifi123456' || empty($ssid)) {
    echo "参数错误";
    exit;
}

$ssid = escapeshellarg($ssid);
$pwd = escapeshellarg($pwd);

$result = shell_exec("sudo nmcli device wifi connect $ssid password $pwd 2>&1");

if (strpos($result, 'success') !== false || strpos($result, '已连接') !== false || trim($result) == '') {
    echo "连接成功";
} else {
    echo "连接失败：密码错误或网络无法连接";
}
?>
