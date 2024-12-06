import os
import smtplib
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

# 教务系统账号密码
username = ""
password = ""

# Cookie存储路径
storage_state_path = "" # \替换为/

# 配置邮件发送信息
smtp_server = ""        # SMTP服务器地址
smtp_port = ""          # SMTP端口号
sender_email = ""       # 发件人邮箱地址
sender_password = ""    # 发件人邮箱的授权密码或应用专用密码
sender_name = ""        # 发件人显示名称
receiver_email = ""     # 收件人邮箱地址

with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch(headless=True)
    
    # 检查 Cookie 是否存在
    if os.path.exists(storage_state_path):
        print(f"检测到Cookie: {storage_state_path}")
        context = browser.new_context(storage_state=storage_state_path)
    else:
        print(f"未检测到Cookie 创建新的会话")
        context = browser.new_context()

    # 使用 context 创建新的页面
    page = context.new_page()

    # 访问目标网页
    page.goto("https://bkjwtest.guet.edu.cn/student/for-std/exam-arrange")

    # 检测是否需要登录
    if page.query_selector('.loginFont_a[href="/authserver/login?type=userNameLogin"]'):
        print("检测到登录")

        # 自动短信验证登录
        page.fill('#username', username)
        page.fill('#password', password)
        page.check('#rememberMe')
        page.click('#login_submit.login-btn.lang_text_ellipsis')
        page.click('#changeReAuthTypeButton.btn.dropdown-toggle.color-dark-blue-title.header-drop-btn')
        page.click('[id="3"].dropdown-item.changeReAuthTypes')
        page.click('#getDynamicCode.dynamicCode_btn.auth_login_btn')
        captcha_code = input("请输入验证码：")
        page.fill('#dynamicCode', captcha_code)
        page.click('#reAuthSubmitBtn.auth_login_btn.submit_btn')
        page.click('.trust-device-button.trust-device-sub-btn')

        # 检测登录是否成功
        try:
            page.wait_for_selector('.jss60.MuiBox-root.css-skle1w', timeout=10000)
            print("登录成功")
            context.storage_state(path=storage_state_path)  # 保存Cookie
            print("成功保存Cookie")
        except Exception as e:
            print("登录失败")
            browser.close()
            exit()

        # 进入本科教学信息平台学生端 否则无法获取考试信息
        page.wait_for_selector('.MuiBox-root.css-d1hnu5[title="本科教学信息平台学生端"]')
        page.click('.MuiBox-root.css-d1hnu5[title="本科教学信息平台学生端"]')

        # 等待页面加载并进入考试信息页
        page.wait_for_timeout(500)
        page = context.new_page()
        page.goto("https://bkjwtest.guet.edu.cn/student/for-std/exam-arrange")

    # 使用 BeautifulSoup 提取信息
    content = page.content()  # 获取页面的完整 HTML 内容
    soup = BeautifulSoup(content, 'lxml-xml')
    exam_elements = soup.find_all('tr', class_='unfinished')

    # 遍历并提取信息
    for exam in exam_elements:
        time = exam.find('div', class_='time ').text.strip()
        location_elements = exam.find_all('span')
        location = ' '.join([elem.text.strip() for elem in location_elements[:3]])
        subject = exam.find('span', style="font-size: 14px; line-height:24px; font-weight: bold;").text.strip()
        type_of_exam = exam.find('span', class_='tag-span type2').text.strip()
        status = exam.find('td', class_='text-center').text.strip()

        # 输出信息
        print(f"时间：{time}")
        print(f"考场：{location}")
        print(f"科目：{subject}")
        print(f"类型：{type_of_exam}")
        print(f"状态：{status}")

        # 格式化邮件内容
        email_content = f"""
        时间：{time}
        考场：{location}
        科目：{subject}
        类型：{type_of_exam}
        状态：{status}
        """

        # 创建邮件内容
        msg = MIMEMultipart()
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = receiver_email
        msg['Subject'] = "未结束的考试提醒"
        msg.attach(MIMEText(email_content, 'plain'))  # 将邮件正文添加到邮件中

        # 使用 SMTP 发送邮件
        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, sender_password)  # 登录 SMTP 服务器
                server.send_message(msg)  # 发送邮件
            print("邮件已发送")
        except Exception as e:
            print(f"发送邮件失败：{e}")

    # 关闭浏览器
    browser.close()