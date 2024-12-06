> ⚠️本脚本在第一次运行时需要手动输入验证码，登录成功后会保存Cookie到配置的路径，之后再运行本脚本会读取成功登录保存的Cookie从而实现跳过登录
# 安装依赖
```bash
pip install playwright lxml beautifulsoup4
playwright install
```
# 使用
编辑脚本中的配置信息：

    # 教务系统账号密码
    username = ""
    password = ""

    # Cookie存储路径
    storage_state_path = "" # 用来储存和读取Cookie \替换为/

    # SMTP服务器配置
    smtp_server = ""    # SMTP服务器地址 此地址用于发送电子邮件 需根据所用邮箱服务提供商选择正确的服务器 例如：
                    # - 对于qq邮箱：smtp.qq.com
                    # - 对于163邮箱：smtp.163.com
                    # - 对于Gmail：smtp.gmail.com
                    # - 对于Outlook：smtp.office365.com
                    # 在使用SMTP服务器时 请确保服务器地址与您的邮箱服务提供商的设置匹配
    smtp_port = ""      # SMTP端口号 用于定义连接到SMTP服务器的端口 确保邮件传输的安全性 常见端口包括：
                    # - 端口 465：用于SSL/TLS加密连接 保证数据传输的安全性
                    # - 端口 587：用于STARTTLS加密连接 从明文开始然后升级为加密连接 适用于大多数邮件服务提供商
                    # 根据您的SMTP服务器配置选择正确的端口
    # 发件人邮箱账户配置
    sender_email = ""       # 发件人的完整邮箱地址 该地址用于登录SMTP服务器并作为发件人身份
    sender_password = ""    # 发件人邮箱的授权密码或应用专用密码 用于验证发件人身份以登录SMTP服务器
    sender_name = ""        # 发件人显示名称
    # 收件人邮箱地址配置
    receiver_email = ""     # 收件人的完整邮箱地址 此地址是邮件发送的目标 确保正确无误 以便邮件能够成功发送

例如：

    # 教务系统账号密码
    username = "2200810114"
    password = "password"

    # Cookie存储路径
    storage_state_path = "C:/Users/username/Playwright/storage_state.json" # \替换为/

    # 配置邮件发送信息
    smtp_server = "smtp.163.com"
    smtp_port = "465"
    sender_email = "123456789@163.com"
    sender_password = "password"
    sender_name = "username"
    receiver_email = "987654321@qq.com"

保存后在shell中输入以下命令运行脚本
```bash
python /path/to/tests.py
```
