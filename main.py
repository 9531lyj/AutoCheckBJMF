import random

import requests
import re
import time
import os
from bs4 import BeautifulSoup
import json
import schedule
from datetime import datetime

# 定义默认的 JSON 数据
default_data = {
    "class": "123",
    "lat": "123",
    "lng": "123",
    "acc": "123",
    "time": 123,
    "cookie": "123",
    "scheduletime": "",
    "pushplus": "123",
    "debug": False
}

# 获取当前目录
current_directory = os.getcwd()
file_name = "data.json"
file_path = os.path.join(current_directory, file_name)

# 检查文件是否存在
if not os.path.exists(file_path):
    # 文件不存在，创建并写入默认数据
    with open(file_path, "w") as file:
        json.dump(default_data, file, indent=4)
    print(f"文件 {file_name} 不存在，已创建并填充默认数据。")

# 读取外部 JSON 文件中的数据
with open('data.json', 'r') as file:
    json_data = json.load(file)
    debug = json_data['debug']
    # 普通用户
    # current_directory = os.getcwd()
    print("----------提醒----------")
    print("原项目地址：https://github.com/JasonYANG170/AutoCheckBJMF")
    print("本项目地址：https://github.com/Yaklo/AutoCheckBJMF")
    print("请查看教程以获取Cookie和班级ID")
    print("data.json文件位置：", current_directory)
    print("----------配置信息(必填)----------")
    if (json_data['class'] == "123"):
        print("请通过查看教程抓包获取班级ID")
        ClassID = input("请输入班级ID：")
    else:
        ClassID = json_data['class']
    print("输入的经纬度格式为x.x，请输入至少8位小数，不满8位用0替补")
    print("腾讯坐标拾取工具：https://lbs.qq.com/getPoint/")
    if (json_data['lat'] == "123"):
        X = input("请输入纬度：")
    else:
        X = json_data['lat']
    if (json_data['lng'] == "123"):
        Y = input("请输入经度：")
    else:
        Y = json_data['lng']
    if (json_data['acc'] == "123"):
        ACC = input("请输入海拔：")
    else:
        ACC = json_data['acc']  # input("请输入海拔：")
    print("----------配置Cookie----------")
    print("请通过查看教程抓包获取Cookie")
    print("教程：https://github.com/JasonYANG170/AutoCheckBJMF/wiki/")
    print("Tip:90%的失败由Cookie变更导致")
    if (json_data['cookie'] == "123"):
        cookies = []
        print("请输入你的Cookie，输入空行结束，支持用户备注格式如下")
        print("username=<备注>;remember....<魔方Cookie>")
        while True:
            cookie = input("Cookie: ")
            if not cookie:
                break
            cookies.append(cookie)
        MyCookie = cookies
    else:
        MyCookie = json_data['cookie']  # int(input("请输入检索时长，建议>60s："))

    # 给定的长字符串

    if (json_data['time'] == 123):
        # SearchTime = int(input("请输入检索间隔，建议>=60s："))
        print("配置完成，您的信息将写入json文件，下次使用将直接从json文件导入")

        # 1. 读取JSON文件
        # JSON文件路径
        file_name = "data.json"
        file_path = os.path.join(current_directory, file_name)
        with open(file_path, "r") as file:
            data = json.load(file)

        # 2. 修改数据
        data["class"] = ClassID
        data["lat"] = X
        data["lng"] = Y
        data["acc"] = ACC
        # data["time"] = SearchTime
        data["time"] = 223
        data["cookie"] = MyCookie

        # 3. 写回JSON文件
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        print("数据已保存到"+current_directory+"下的data.json中。")

    else:
        SearchTime = json_data['time']  # int(input("请输入检索时长，建议>60s："))

    print("----------配置定时任务(可选)----------")
    print("格式为00:00,不设置定时请留空")
    print("Tip：请注意以上格式并使用英文符号“:”不要使用中文符号“：”")
    if (json_data['scheduletime'] == ""):
        scheduletime = input("请输入开启时间：")
    else:
        scheduletime = json_data['scheduletime']  # int(input("请输入检索时长，建议>60s："))
    print("----------配置通知(可选)----------")
    if (json_data['pushplus'] == "123"):
        token = input("请输入pushplus推送密钥,不需要请留空,或输入off永久关闭该提示：")
        if(token!=""):
        # 1. 读取JSON文件
        # JSON文件路径
            file_name = "data.json"
            file_path = os.path.join(current_directory, file_name)
            with open(file_path, "r") as file:
                data = json.load(file)

        # 2. 修改数据
            data["pushplus"] = token
        # 3. 写回JSON文件
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

            print("数据已保存到" + current_directory + "下的data.json中。")

    else:
        token = json_data['pushplus']  # input("请输入pushplus密钥：")
    print("----------信息----------")
    print("班级ID:" + ClassID)
    print("经度:" + Y)
    print("纬度:" + X)
    print("海拔:" + ACC)
    print("检索间隔:" + str(SearchTime))
    print("Cookie数量:" + str(len(MyCookie)))
    print("定时:" + scheduletime)
    print("通知token:" + token)
    print("---------------------")
# 输出用户输入的内容
print("一切就绪，程序开始执行")



# GitHub Actions自动任务
# ClassID = os.environ['ClassID']
# X = os.environ['X']
# Y = os.environ['Y']
# ACC = os.environ['ACC']
# SearchTime = os.environ['SearchTime']
# MyCookie = os.environ['MyCookie']
# token = os.environ['token']
#scheduletime = os.environ['scheduletime']

# 本地面板运行
#ClassID = ''
#X = ''
#Y = ''
#ACC = ''
#SearchTime = 60
#MyCookie = ''
#token = ''  #在pushplus网站中可以找到
#scheduletime =''

# 随机经纬，用于定位偏移
def modify_decimal_part(num):
    num = float(num)
    print(num)
    # 将浮点数转换为字符串
    num_str = f"{num:.8f}"  # 确保有足够的小数位数
    # 找到小数点的位置
    decimal_index = num_str.find('.')
    # 提取小数点后4到6位
    decimal_part = num_str[decimal_index + 4:decimal_index + 9]
    # 将提取的小数部分转换为整数
    decimal_value = int(decimal_part)
    # 生成一个在-150到150范围的随机整数
    random_offset = random.randint(-15000, 15000)
    # 计算新的小数部分
    new_decimal_value = decimal_value + random_offset
    # 将新的小数部分转换为字符串，并确保它有3位
    new_decimal_str = f"{new_decimal_value:05d}"
    # 拼接回原浮点数
    new_num_str = num_str[:decimal_index + 4] + new_decimal_str + num_str[decimal_index + 9:]
    # 将新的字符串转换回浮点数
    new_num = float(new_num_str)

    return new_num

def job():
    current_time = datetime.now()
    print("进入检索，当前时间为:", current_time)
    title = '班级魔法自动签到任务'  # 改成你要的标题内容
    url = 'http://k8n.cn/student/course/' + ClassID + '/punchs'

    for jobs in range(0,2):
        nojobs = 0
        # 多用户检测签到
        for uid in range(0,len(MyCookie)):
            onlyCookie = MyCookie[uid]

            # 使用正则表达式提取目标字符串 - 用户备注
            pattern = r'username=[^;]+'
            result = re.search(pattern, onlyCookie)

            if result:
                username_string = result.group(0).split("=")[1]
            else:
                username_string = ""

            # 用户信息显示
            if username_string != "":
                print("★★★★★ 用户UID：%d <%s> 开始签到 ★★★★★"%(uid+1,username_string))
            else:
                print("★★★★★ 用户UID：%d 开始签到 ★★★★★"%(uid+1))

            # 使用正则表达式提取目标字符串 - Cookie
            pattern = r'remember_student_59ba36addc2b2f9401580f014c7f58ea4e30989d=[^;]+'
            result = re.search(pattern, onlyCookie)

            if result:
                extracted_string = result.group(0)
                if debug:
                    print(extracted_string)
            else:
                print("未找到匹配的字符串,检查Cookie是否错误")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9; AKT-AK47 Build/USER-AK47; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20231202 MMWEBID/1136 MicroMessenger/8.0.47.2560(0x28002F35) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'X-Requested-With': 'com.tencent.mm',
                'Referer': 'http://k8n.cn/student/course/' + ClassID,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh-SG;q=0.9,zh;q=0.8,en-SG;q=0.7,en-US;q=0.6,en;q=0.5',
                'Cookie': extracted_string
            }

            response = requests.get(url, headers=headers)
            print("响应:", response)

            # 创建 Beautiful Soup 对象解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 使用正则表达式从 HTML 文本中提取所有 punch_gps() 中的数字
            pattern = re.compile(r'punch_gps\((\d+)\)')
            matches = pattern.findall(response.text)
            print("找到GPS定位签到:", matches)
            pattern2 = re.compile(r'punchcard_(\d+)')
            matches2 = pattern2.findall(response.text)
            print("找到扫码签到:", matches2)
            matches.extend(matches2)
            if matches:
                for match in matches:
                    print(match)
                    url1 = "http://k8n.cn/student/punchs/course/" + ClassID + "/" + match
                    payload = {
                        'id': match,
                        'lat': modify_decimal_part(X),
                        'lng': modify_decimal_part(Y),
                        'acc': ACC,  #未知，可能是高度
                        'res': '',  #拍照签到
                        'gps_addr': ''  #未知，抓取时该函数为空
                    }

                    response = requests.post(url1, headers=headers, data=payload)

                    if response.status_code == 200:
                        print("请求成功")
                        print("响应:", response)

                        # 解析响应的 HTML 内容
                        soup_response = BeautifulSoup(response.text, 'html.parser')
                        # h1_tag = soup_response.find('h1')
                        div_tag = soup_response.find('div', id='title')

                        if debug:
                            print("★☆★")
                            print(soup_response)
                            print("===")
                            print(div_tag)
                            print("★☆★")

                        if div_tag:
                            h1_text = div_tag.text
                            print(h1_text)
                            # encoding:utf-8
                            if token != "" and h1_text== "签到成功" and token != "off":
                                url = 'http://www.pushplus.plus/send?token=' + token + '&title=' + title + '&content=' + h1_text  # 不使用请注释
                                requests.get(url)  # 不使用请注释
                            continue  # 返回到查找进行中的签到循环
                        else:
                            print("未找到 <h1> 标签，可能存在错误")
                    else:
                        print("请求失败，状态码:", response.status_code)
                        nojobs+=1 # 记录失败次数
            else:
                print("未找到在进行的签到")
            # 可以设置一个间隔时间，避免过于频繁地请求
            # time.sleep(SearchTime)  # 暂停10秒后重新尝试
            time.sleep(5) #暂停5秒后尝试下一个Cookie签到
        if (nojobs > 0) :
            jobs-=1 #检测到存在签到失败，延长重试规则
            print("本次签到存在异常，异常次数%d，已自动延长重试次数"%nojobs)
        time.sleep(300) #等待5分钟后进行重复签到，避免签到失败
    print("☆本次签到结束，等待设定的时间%s到达☆"%scheduletime)

# job()
if (scheduletime != ""):
    print("等待设定时间" + scheduletime + "到达")
    # 设置定时任务，在每天的早上8点触发
    schedule.every().day.at(scheduletime).do(job)

    while True:
        schedule.run_pending()
        time.sleep(10)
else:
    job()
