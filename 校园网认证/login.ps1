$account = ""          # 在此填写学号
$password = ""         # 在此填写密码
$operator = ""         # 在此填写运营商（校园网为空，移动:@cmcc，联通:@unicom，电信:@telecom）
$wireless =      # 填写网络连接方式，无线为 $true，有线为 $false

if($wireless)
{
    # 将密码编码为 Base64
    $passwordBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($password))
    # Write-Output "$passwordBase64"

    # 获取 Wi-Fi 网络配置信息
    $wifiInfo = Get-NetIPConfiguration | Where-Object { 
        $_.InterfaceAlias -like "*Wi-Fi*" -or $_.InterfaceAlias -like "*WLAN*" -and $_.IPv4Address -ne $null 
    }

    if ($wifiInfo) {
        # 选择第一个匹配的网络接口
        $firstWiFi = $wifiInfo | Select-Object -First 1
        $ip = $firstWiFi.IPv4Address.IPAddress
        $mac = ($firstWiFi.NetAdapter.MacAddress -replace "-", "").ToLower()

        # 构造 URL
        $url = "http://10.0.1.5:801/eportal/portal/login?callback=dr1003&login_method=1&user_account=,0,$account$operator&user_password=$passwordBase64&wlan_user_ip=$ip&wlan_user_ipv6=&wlan_user_mac=$mac&wlan_ac_ip=10.32.255.10&wlan_ac_name=HJ-BRAS-ME60-01&jsVersion=4.2&terminal_type=1&lang=zh&lang=zh&v=8405"
        Write-Output "$url"

        # 发出 HTTP 请求
        Invoke-WebRequest -Uri $url
    }
    else { Write-Error "未找到有效的网络信息"}
}  
else
{
    # 构造 URL
    $url = "http://10.0.1.5/drcom/login?callback=dr1003&DDDDD=$account$operator&upass=$password"
    Write-Output "$url"

    # 发出 HTTP 请求
    Invoke-WebRequest -Uri $url
}
