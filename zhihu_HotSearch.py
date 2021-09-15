import requests
import json
import datetime
import threading


def fun_timer():
    hotUrl = 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/86.0.4240.198 Safari/537.36'}
    allResponse = requests.get(hotUrl, headers=headers).text
    jsonDecode = json.loads(allResponse)
    nowtime = datetime.datetime.now()
    str_time = nowtime.strftime('%Y-%m-%d %H:%M:%S')
    f = open(r"C:\Users\lyy\Desktop\2021.9.13_zhihu_HotSearch.txt", "a")
    f.write(str_time)
    f.write("\n")
    print(str_time)
    for i in range(50):
        print(
            str(i + 1) + '.' + jsonDecode["data"][i]["target"]["title"] +
            ' https://www.zhihu.com/question/' +
            str(jsonDecode["data"][i]["target"]["id"]))
        f.write(
            str(i + 1) + '.' + jsonDecode["data"][i]["target"]["title"] +
            ' https://www.zhihu.com/question/' +
            str(jsonDecode["data"][i]["target"]["id"]))
        f.write("\n")
    f.write("\n")
    # 关闭打开的文件
    f.close()
    print()
    global timer
    timer = threading.Timer(300, fun_timer)
    timer.start()


timer = threading.Timer(1, fun_timer)
timer.start()
