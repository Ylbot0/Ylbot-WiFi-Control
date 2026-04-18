<?php
$key = $_GET['key'] ?? '';
if ($key !== 'wifi123456') exit;

$hostname = php_uname('n');
$cpu = trim(shell_exec("top -bn1 | grep 'Cpu(s)' | awk '{print 100 - \$8\"%\"}'"));
$mem = trim(shell_exec("free -h | awk '/Mem/{print \$3\"/\"\$2}'"));
$wifi = trim(shell_exec("nmcli connection show --active | grep wifi | awk '{print \$1}'"));
$ip = trim(shell_exec("hostname -I | awk '{print \$1}'"));

echo "主机名：$hostname\n";
echo "CPU占用：$cpu\n";
echo "内存使用：$mem\n";
echo "当前WiFi：$wifi\n";
echo "本机IP：$ip\n";
?>
