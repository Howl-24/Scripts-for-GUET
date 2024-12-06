import requests
import re
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.utils import formataddr

# 房间信息
room_id = ""  # 房间id

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

# 定义目标URL
url = f"http://sdcx.guet.edu.cn/yktserver/ecardserv/ykt.asmx/GetYDLSByRoomno?roomno={room_id}&n=10"
#print(url)  # 打印URL（可选）

# 发送请求
response = requests.get(url)

# 检查响应的状态码
if response.status_code == 200:
    # 使用lxml解析内容
    soup = BeautifulSoup(response.text, 'lxml-xml')  # 注意：使用'lxml-xml'解析器

    # 提取特定标签内容
    bills = [tag.text.strip() for tag in soup.find_all("ds")]

    # 构建邮件正文
    email_body = ""
    for bill in bills:
        date = re.match(r"\d{4}-\d{2}-\d{2}", bill)  # 匹配日期格式
        remain = re.search(r"\d+\.\d+", bill)  # 匹配电费金额
        if date and remain:
            email_body += f"{date.group()}: {remain.group()}\n"  # 拼接内容
            print(f"{date.group()}: {remain.group()}")  # 打印提取的信息

    # 检查是否有内容需要发送
    if email_body:  # 确保有内容需要发送
        # 准备邮件
        subject = "电费提醒"  # 邮件主题
        message = MIMEText(email_body, "plain", "utf-8")  # 邮件正文内容
        message["Subject"] = subject
        message["From"] = formataddr((sender_name, sender_email))
        message["To"] = receiver_email

        try:
            # 发送邮件
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 使用SSL连接SMTP服务器
            server.login(sender_email, sender_password)  # 登录SMTP服务器
            server.sendmail(
                from_addr=sender_email,  # 发件人地址
                to_addrs=receiver_email,  # 收件人地址
                msg=message.as_string()  # 邮件内容
            )
            print("邮件发送成功！")  # 打印发送成功信息
        except smtplib.SMTPException as e:
            print(f"邮件发送失败：{e}")  # 打印发送失败的异常信息
        finally:
            server.quit()  # 退出SMTP连接
    else:
        print("没有电费数据")  # 如果没有电费数据，打印此信息
else:
    print(f"请求失败 状态码为: {response.status_code}")  # 打印请求失败的状态码