import os
import smtplib
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

# 教学楼 必填
# 科技楼 实训楼 四创中心 文科楼 信科41教学楼 信科42教学楼 信息与通信学院楼 尧山第二教学楼
# 尧山第六教学楼 尧山第三教学楼 尧山第十六教学楼 尧山第十七教学楼 尧山第十三教学楼 
# 尧山第十四教学楼 尧山第十一教学楼 尧山第四教学楼 尧山第五教学楼 尧山第一教学楼 艺术楼 专家楼
teaching_building = ""

# 起始日期 必填
# 今天 明天 或者 YYYY-MM-DD
start_date = "" 

# 选择节次 必填
# 上午 上1,2 上3,4 中午 下午 下5,6 下7,8 晚上 全天
selected_period = "" 

# 教室 可选
classroom = ""

# 容量 可选
capacity = ""

# 教室类型 可选
# 普通 电教室 语音室 机房 实验室
classroom_type = ""

# 结束日期 可选
# YYYY-MM-DD
end_date = ""

# 星期几 可选
weekday = ""  

# 账号密码
username = ""
password = ""

# Cookie存储路径
storage_state_path = ""

# 配置邮件发送信息
smtp_server = ""        # SMTP服务器地址
smtp_port = ""          # SMTP端口号，使用SSL连接
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
    page.goto("https://bkjwtest.guet.edu.cn/student/for-std/room-free")

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
        page.click('.trust-device-button.trust-device-sub-btnj')

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

        # 进入本科教学信息平台学生端 否则无法获取教室信息
        page.wait_for_selector('.MuiBox-root.css-d1hnu5[title="本科教学信息平台学生端"]')
        page.click('.MuiBox-root.css-d1hnu5[title="本科教学信息平台学生端"]')

        # 等待页面加载并进入教室信息页
        page.wait_for_timeout(500)
        page = context.new_page()
        page.goto("https://bkjwtest.guet.edu.cn/student/for-std/room-free")

    # 选择教学楼
    page.fill('#buildingAssoc-selectized', teaching_building)
    page.click(f'text="{teaching_building}"')

    # 选择教室
    if classroom:
        page.fill('#roomAssoc-selectized', classroom)
        page.click(f'text="{classroom}"')

    # 输入容量
    if capacity:
        page.fill('#seatsForLessonGte', str(capacity))  # 将整数转换为字符串

    # 选择教室类型
    if classroom_type:
        page.fill('#roomTypeAssoc-selectized', classroom_type)
        page.click(f'text="{classroom_type}"')

    # 选择起始日期
    if start_date == "今天":
        page.click('button.btn.btn-link.btn-xs:has-text("今天")')
    elif start_date == "明天":
        page.click('button.btn.btn-link.btn-xs:has-text("明天")')
    else:
        page.fill('input.form-control.input[placeholder="起始日期"]', start_date)   # 如果起始日期格式为YYYY-MM-DD 填充输入框

    # 选择结束日期
    if end_date:
        page.fill('input.form-control.input[placeholder="结束日期"]', end_date)

    # 选择星期几
    if weekday:
        page.click('.btn-group.bootstrap-select.show-tick')
        page.click(f'span.text:has-text("{weekday}")')

    # 选择节次
    page.click(f'button.btn.btn-link.btn-xs:has-text("{selected_period}")')

    # 查询
    page.click('.btn.btn-primary')
    page.wait_for_timeout(500)

    # 使用 BeautifulSoup 提取信息
    content = page.content()  # 获取页面的完整 HTML 内容
    all_email_content = ""  # 初始化一个字符串来存储所有提取的信息
    soup = BeautifulSoup(content, 'lxml-xml')
    rows = soup.find_all('tr')  # 遍历每一行 <tr> 标签
    for row in rows:
        cells = row.find_all('td')  # 找到每一行的 <td> 标签
        if len(cells) == 7:  # 检查是否有7个 <td> 标签
            # 提取并格式化信息
            classroom_name = cells[0].text.strip()
            campus = cells[1].text.strip()
            building = cells[2].text.strip()
            floor = cells[3].text.strip()
            seat_count = cells[4].text.strip()
            room_type = cells[5].text.strip()
            remarks = cells[6].text.strip()

            # 打印提取的信息
            print(f"{classroom_name}\t{campus}\t{building}\t{floor}\t{seat_count}\t{room_type}\t{remarks}")

            # 将提取的信息格式化并追加到 all_email_content 中
            all_email_content += f"""
            教室名称：{classroom_name}
            校区：{campus}
            教学楼：{building}
            楼层：{floor}
            上课用座位数：{seat_count}
            教室类型：{room_type}
            备注：{remarks}
            """

    # 创建邮件内容
    msg = MIMEMultipart()
    msg['From'] = formataddr((sender_name, sender_email))
    msg['To'] = receiver_email
    msg['Subject'] = "空闲教室"
    msg.attach(MIMEText(all_email_content, 'plain'))  # 将合并的内容作为邮件正文

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