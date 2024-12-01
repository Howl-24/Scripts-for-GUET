#!/bin/bash

# 配置参数
account=""          # 在此填写学号
password=""         # 在此填写密码
operator=""         # 在此填写运营商（校园网为空，移动:@cmcc，联通:@unicom，电信:@telecom）
wireless=        # true 表示无线连接，false 表示有线连接

if $wireless; then
    # Base64 编码密码
    passwordBase64=$(echo -n "$password" | base64)

    # 获取 Wi-Fi IP 和 MAC 地址
    wifi_info=$(ip -o addr show | grep "wlan" | grep -Eo 'inet [^ ]+' | awk '{print $2}')
    mac_address=$(ip link show | grep "wlan" | grep -oE '([[:xdigit:]]{2}:){5}[[:xdigit:]]{2}' | head -n 1 | tr '[:upper:]' '[:lower:]')

    ip_address=${wifi_info%%/*}  # 提取 IP 地址部分

    # 构造 URL
    url="http://10.0.1.5:801/eportal/portal/login?callback=dr1003&login_method=1&user_account=,0,${account}${operator}&user_password=${passwordBase64}&wlan_user_ip=${ip_address}&wlan_user_ipv6=&wlan_user_mac=${mac_address}&wlan_ac_ip=10.32.255.10&wlan_ac_name=HJ-BRAS-ME60-01&jsVersion=4.2&terminal_type=1&lang=zh&lang=zh&v=8405"

    # 打印 URL（可选）
    echo "$url"

    # 发出 HTTP 请求
    curl "$url"
else
    # 构造 URL
    url="http://10.0.1.5/drcom/login?callback=dr1003&DDDDD=${account}${operator}&upass=${password}"

    # 打印 URL（可选）
    echo "$url"

    # 发出 HTTP 请求
    curl "$url"
fi
