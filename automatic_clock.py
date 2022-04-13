# -*- coding: utf-8 -*-
"""
# @Author: 狄克
# @Time  : 2020/5/1 23:24
# @File  : automatic_clock.py

实现自动登陆疫情打卡页面并签到
工具说明：使用 Python3 + Selenium + ChromeDriver
执行方式: python3 automatic_clock.py [host] [user] [password] [database]
使用linux定时任务: crontab -e
"""
import datetime
import sys
import pymysql as pymysql
import yagmail as yagmail
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

url = "http://login.cuit.edu.cn/Login/xLogin/Login.asp"
NewTask_XPath = "/html/body/div[2]/table/tbody[2]/tr[2]/td[2]/a"
Work_XPath = "//*[@id='wjTA']/tbody/tr[4]/td[2]/div/select[3]"
Health_XPath = "//*[@id='wjTA']/tbody/tr[4]/td[2]/div/select[4]"
Life_XPath = "//*[@id='wjTA']/tbody/tr[4]/td[2]/div/select[5]"
Family_XPath = "//*[@id='wjTA']/tbody/tr[4]/td[2]/div/select[6]"
Submit_XPath = "/html/body/form/div[1]/table/tbody/tr/td[1]/input"


# chrome浏览器启动配置
def get_options():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

    return chrome_options


def get_students(host, user, password, database):
    student_list = None
    try:
        db = pymysql.connect(host=host, user=user, password=password, database=database)  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor方法获取操作游标
        sql = "select name, username, password, email from student"  # sql查询语句
        cursor.execute(sql)  # 使用 execute 方法执行SQL语句
        student_list = cursor.fetchall()
        db.close()  # 关闭连接; 关闭后无法再进行操作，除非再次创建连接
    except Exception as e:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        do_send_mail('1138832931@qq.com', "{}\n数据库查询失败，任务终止\n错误信息: {}".format(now_time, e))

    return student_list


def do_send_mail(mail, content):
    yag = yagmail.SMTP("dike1138832931@126.com", "GVVEZOBIJCRVNQWO", 'smtp.126.com')
    yag.send(mail, "打卡提醒", content)


# 登陆
def do_login(name, password):
    # 找到登录框 输入账号密码
    driver.implicitly_wait(20)
    driver.find_element(By.ID, 'txtId').send_keys(name)
    driver.find_element(By.ID, 'txtMM').send_keys(password)
    # 模拟点击登录
    driver.find_element(By.ID, 'IbtnEnter').click()


# 打卡
def do_sign():
    driver.implicitly_wait(20)
    driver.find_element(By.XPATH, NewTask_XPath).click()  # 打开最新打卡任务
    driver.implicitly_wait(20)
    # 定位select框 进行选择
    Select(driver.find_element(By.XPATH, Work_XPath)).select_by_index(3)
    Select(driver.find_element(By.XPATH, Health_XPath)).select_by_index(1)
    Select(driver.find_element(By.XPATH, Life_XPath)).select_by_index(1)
    Select(driver.find_element(By.XPATH, Family_XPath)).select_by_index(1)
    # 提交打卡 处理Alert弹出框
    driver.find_element(By.XPATH, Submit_XPath).click()
    driver.switch_to.alert.accept()


if __name__ == '__main__':
    sql_host, sql_user, sql_password, sql_database = sys.argv[1:5]
    students = get_students(sql_host, sql_user, sql_password, sql_database)
    driver = webdriver.Chrome(options=get_options())
    for item in students:
        student = {
            'name': item[0],
            'username': item[1],
            'password': item[2],
            'email': item[3]
        }
        driver.get(url)
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            print(student['name'], end="-->")
            do_login(student['username'], student['password'])
            do_sign()
            print("{}打卡成功".format(student['name']))
            do_send_mail(student['email'], "{}\n{}打卡成功".format(nowTime, student['name']))
            driver.execute_script('document.querySelector("body > form > div:nth-child(1) > table > tbody > tr > '
                                  'td:nth-child(1) > a").click();')
            driver.implicitly_wait(10)
            driver.execute_script('document.querySelector("body > div:nth-child(1) > table > tbody > tr > '
                                  'td:nth-child(2) > a").click();')
            driver.switch_to.alert.accept()
        except Exception as e:
            print("{}打卡失败\n错误信息: {}".format(student['name'], e))
            do_send_mail(student['email'], "{}\n{}打卡失败\n错误信息: {}".format(nowTime, student['name'], e))
    driver.quit()
