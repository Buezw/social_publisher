from playwright.sync_api import sync_playwright
import time
import re
import os

# 文件路径，用于保存会话状态
session_file = r"session.json"
user_input = input("标题和书名，用空格分隔：")
title_text, book_name = user_input.split()

# 打开并读取 HTML 文件内容
with open(r'social_graph.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用变量替换 HTML 中的内容
#html_with_variables = re.sub(r'英文', english_text, html_content)
html_with_variables = re.sub(r'标题', title_text, html_content)
html_with_variables = re.sub(r'书名', book_name, html_with_variables)
tag = ['#读书']
# 将修改后的内容写回 HTML 文件
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(html_with_variables)

print("HTML 文件已更新")

time.sleep(1)
with sync_playwright() as p:
    # 启动浏览器并创建一个新的上下文

    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
        
    # 本地 HTML 文件的相对路径
    local_file_path = os.path.abspath("output.html")
    file_url = f"file://{local_file_path}"

    page = context.new_page()
    page.goto(file_url)

    page.wait_for_load_state("networkidle")
    print("本地 HTML 文件的可视区域已转换为 PNG 并保存为 output.png")


    page.set_viewport_size({"width": 800, "height": 600})
    # 等待页面加载完成
    page.wait_for_load_state("networkidle")
    # 截图保存为 PNG 文件（仅可视区域）
    page.screenshot(path="output.png")
    browser.close()

def load_session():
    with sync_playwright() as p:
        # 使用保存的会话状态文件创建新的上下文
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=session_file)
        file_input_xpath = "xpath=/html/body/div[1]/div/div[2]/div/div[2]/main/div[3]/div/div/div[1]/div/div/div/div[1]/div[2]"
        # 打开页面，加载登录后的状态
        page = context.new_page()
        page.goto("https://creator.xiaohongshu.com/publish/publish?source=official")  # 替换为实际的目标页面 URL
        page.wait_for_selector(file_input_xpath, timeout=60000)
        page.locator(file_input_xpath).click()
        upload_address = 'xpath=/html/body/div[1]/div/div[2]/div/div[2]/main/div[3]/div/div/div[1]/div/div/div/div[2]/div[1]/div/input'
        page.locator(upload_address).set_input_files("output.png")
        page.locator('xpath=/html/body/div[1]/div/div[2]/div/div[2]/main/div[3]/div/div/div[1]/div/div/div/div/div[1]/div[1]/div[4]/div[1]/div/input').fill(book_name)
        tag_input = 'xpath=/html/body/div[1]/div/div[2]/div/div[2]/main/div[3]/div/div/div[1]/div/div/div/div/div[1]/div[1]/div[5]/p'
        tag_clicker = 'xpath=/html/body/div[1]/div/div[2]/div/div[2]/main/div[3]/div/div/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div[5]/div[4]/div/div[1]/ul/li[1]'
        # for i in tag:
        #     page.locator(tag_input).fill(i)
        #     page.wait_for_selector(tag_clicker, timeout=60000)
        #     page.locator(tag_input).click()
        page.locator(tag_input).fill(title_text)
        # 检查登录状态（例如截屏验证）
        #input('wait')
        time.sleep(5)
        page.locator('xpath=/html/body/div[1]/div/div[2]/div/div[2]/main/div[3]/div/div/div[1]/div/div/div/div/div[2]/div/button[1]').click()
        #/html/body/div[1]/div/div[2]/div/div[2]/main/div[3]/div/div/div[1]/div/div/div/div/div[2]/div/button[1]
        time.sleep(5)
        page.screenshot(path="output.png")
        print("已发布！")

        browser.close()


def save_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # 打开页面并登录（此处替换为实际的登录页面 URL）
        page = context.new_page()
        page.goto("https://creator.xiaohongshu.com/publish/publish?source=official")

        input("123")
        # 等待登录完成，确保页面已加载
        page.wait_for_load_state("networkidle")

        # 保存会话状态到文件
        context.storage_state(path=session_file)
        
        browser.close()

# 调用函数：首次运行时保存会话，以后可以直接加载
#save_session()  # 手动登录并保存会话
load_session()  # 使用保存的会话直接加载
