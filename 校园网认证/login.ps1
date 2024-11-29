$accountc = ""          # ""中填学号
$password = ""          # ""中填密码
$operator = ""          # ""中填运营商 校园网为空 移动:@cmcc 联通:@unicom 电信:@telecom
$wireless = [bool]$     # $后填网络连接方式 无线:true 有线:false

if($wireless)
{
    # Encode the password to Base64
    $passwordBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($password))
    # Write-Output "$passwordBase64"

    # Get the Wi-Fi network configuration
    $wifiInfo = Get-NetIPConfiguration | Where-Object { 
        $_.InterfaceAlias -like "*Wi-Fi*" -or $_.InterfaceAlias -like "*WLAN*" -and $_.IPv4Address -ne $null 
    }

    # Extract and format Wi-Fi IP and MAC Address
    $wifiInfo | ForEach-Object {
        $ip = $_.IPv4Address.IPAddress
        $mac = ($_.NetAdapter.MacAddress -replace "-", "").ToLower()
        # Write-Output "$ip"
        # Write-Output "$mac"
    }

    # Construct the URL
    $url = "http://10.0.1.5:801/eportal/portal/login?callback=dr1003&login_method=1&user_account=,0,$account$operator&user_password=$passwordBase64&wlan_user_ip=$ip&wlan_user_ipv6=&wlan_user_mac=$mac&wlan_ac_ip=10.32.255.10&wlan_ac_name=HJ-BRAS-ME60-01&jsVersion=4.2&terminal_type=1&lang=zh&lang=zh&v=8405"
    # Write-Output "$url"

    # Make the HTTP request
    Invoke-WebRequest -Uri $url

    return
}  
else
{
    # Construct the URL
    $url = "http://10.0.1.5/drcom/login?callback=dr1003&DDDDD=$account$operator&upass=$password"
    # Write-Output "$url"

    # Make the HTTP request
    Invoke-WebRequest -Uri $url

    return
}
