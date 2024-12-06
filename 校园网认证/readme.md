# login.ps1
本脚本适用于windows
## 使用
编辑脚本中的配置信息：
    $account = ""          # 在此填写学号
    $password = ""         # 在此填写密码
    $operator = ""         # 在此填写运营商（校园网为空，移动:@cmcc，联通:@unicom，电信:@telecom）
    $wireless =            # 填写网络连接方式，无线为 $true，有线为 $false

例如：
    $account = "2200810114"       # 学号
    $password = "1919810"         # 密码
    $operator = "@unicom"         # 此处为联通
    $wireless = $true             # 此处为无线网络

    $account = "2200810114"       # 学号
    $password = "1919810"         # 密码
    $operator = ""                # 留空为校园网
    $wireless = $false            # 此处为有线网络

保存后右键脚本，点击使用 powershell 运行
## 开机自动运行
打开任务计划程序：
    按 Win + R，输入 taskschd.msc，然后回车。

创建一个任务：
    在右侧点击“创建任务”。

配置任务：
    常规选项卡：
        为任务命名，比如 10.0.1.5login。
    触发器选项卡：
        点击“新建”，设置为“在系统启动时”触发。
    操作选项卡：
        点击“新建”。
        动作选择“启动程序”。
        在“程序或脚本”框中，输入以下内容：
```pwsh
powershell.exe
```
在“添加参数”框中，输入以下内容：
```pwsh
-ExecutionPolicy Bypass -File "C:\Path\To\YourScript.ps1"
```
（将 C:\Path\To\YourScript.ps1 替换为你的脚本路径。）

# login.sh
本脚本适用于linux
## 使用
编辑脚本中的配置信息：
    account=""          # 在此填写学号
    password=""         # 在此填写密码
    operator=""         # 在此填写运营商（校园网为空，移动:@cmcc，联通:@unicom，电信:@telecom）
    wireless=           # true 表示无线连接，false 表示有线连接

例如：
    account = "2200810114"       # 学号
    password = "1919810"         # 密码
    operator = "@unicom"         # 此处为联通
    wireless = $true             # 此处为无线网络

    account = "2200810114"       # 学号
    password = "1919810"         # 密码
    operator = ""                # 留空为校园网
    wireless = $false            # 此处为有线网

保存后在shell中输入
```bash
bash /path/to/login.sh
```
## 使用systemd开机自动运行
创建服务文件：
```bash
sudo nano /etc/systemd/system/login.service：
```

配置服务：
    在文件中添加以下内容：
```bash
[Unit]
Description=login to 10.0.1.5
After=network.target

[Service]
Type=oneshot
ExecStart=/bin/bash /path/to/your/login.sh
User=root

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl enable login.service
```

启动并测试服务：
```bash
sudo systemctl start login.service
```
