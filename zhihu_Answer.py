import os
import pandas as pd
from selenium import webdriver
from lxml import etree
import time
import jieba
import re
import numpy as np

url1 = input("https://www.zhihu.com/question/486510054")

browser = webdriver.Chrome("C:/Program Files (x86)/Google/Chrome/Application")
browser.get(url1)

try:
    button1 = browser.find_elements_by_xpath("""//div[@class= "QuestionHeader-detail"]
    //button[contains(@class,"Button") and contains(@class,"QuestionRichText-more")and contains(@class , "Button--plain")]""")[0]
    button1.click()
except IOError:
    print('这个问题比较简单，并没有问题的全部内容哦！')

# 此网页就属于异步加载的情况
# 那么我们就需要多次下滑
for i in range(20):
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(0.5)
    print(i)
button2 = browser.find_elements_by_xpath("""//button[@aria-label = '关闭']""")[0]
button2.click()

final_end_it = browser.find_elements_by_xpath("""//button[contains(@class,"Button") 
    and contains(@class ,'QuestionAnswers-answerButton') 
    and contains(@class ,'Button--blue')
    and contains(@class ,'Button--spread')
]""")
while final_end_it == []:
    final_end_it = browser.find_elements_by_xpath("""//button[contains(@class,"Button") 
    and contains(@class ,'QuestionAnswers-answerButton') 
    and contains(@class ,'Button--blue')
    and contains(@class ,'Button--spread')
]""")
    js = "var q=document.documentElement.scrollTop=0"  
    browser.execute_script(js)
    for i in range(30):
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(0.5)
        print(i)

dom = etree.HTML(browser.page_source)

Followers_number_first = dom.xpath("""//div[@class="QuestionFollowStatus"]//div[@class = "NumberBoard-itemInner"]/strong/text()""")[0]
Browsed_number_first = dom.xpath("""//div[@class="QuestionFollowStatus"]//div[@class = "NumberBoard-itemInner"]/strong/text()""")[1]

# 关注者数量
Followers_number_final = re.sub(",", "", Followers_number_first)

# 浏览数量
Browsed_number_final = re.sub(",", "", Browsed_number_first)

# 问题链接
problem_url = url1

# 问题ID
problem_id = re.findall(r"\d+\.?\d*", url1)

# 问题标题
problem_title = dom.xpath("""//div[@class = 'QuestionHeader']//h1[@class = "QuestionHeader-title"]/text()""")

# 问题点赞数
problem_endorse = dom.xpath("""//div[@class = 'QuestionHeader']//div[@class = "GoodQuestionAction"]/button/text()""")
# 问题评论数
problem_Comment = dom.xpath("""//div[@class = 'QuestionHeader']//div[@class = "QuestionHeader-Comment"]/button/text()""")

# 问题回答数
answer_number = dom.xpath("""//div[@class = 'Question-main']//h4[@class = "List-headerText"]/span/text()""")

# 问题标签
problem_tags_list = dom.xpath("""//div[@class = 'QuestionHeader-topics']//a[@class = "TopicLink"]/div/div/text()""")

# 具体内容
comment_list = dom.xpath("""//div[@class = 'List-item']//div[@class = "RichContent-inner"]""")
comment_list_text = []
for comment in comment_list:
    comment_list_text.append(comment.xpath("string(.)"))

# 发表时间
time_list = dom.xpath("""//div[@class = 'List-item']//div[@class = "ContentItem-time"]//span/@data-tooltip""")
edit_time_list = dom.xpath("""//div[@class = 'List-item']//div[@class = "ContentItem-time"]//span/text()""")

# 点赞数
endorse_list = dom.xpath("""//div[@class = 'List-item']//button[contains(@class,"Button") and contains(@class,"VoteButton") and contains(@class , "VoteButton--up")]/@aria-label""")

# 评论人数
number_of_endorse_list = dom.xpath("""//div[@class = 'List-item']//svg[contains(@class,"Zi") and contains(@class,"Zi--Comment") 
and contains(@class,"Button-zi")]/../../text()""")

# 回答链接
answers_url_list = dom.xpath("""//div[@class = 'List-item']//div[contains(@class,"ContentItem") and contains(@class,"AnswerItem")]
/meta[@itemprop = "url"]/@content""")

authors_list = dom.xpath("""//div[@class = 'List-item']//div[contains(@class,"ContentItem") and contains(@class,"AnswerItem")]
/@data-zop""")

# 作者姓名
authorName_list = []

# 作者id
authorid_list = []
for i in authors_list:
    authorName_list.append(eval(i)['authorName'])
    authorid_list.append(eval(i)["itemId"])

data = pd.DataFrame()

data['具体内容'] = comment_list_text
data["发表时间"] = time_list
data["点赞数"] = endorse_list
data["评论人数"] = number_of_endorse_list
data["回答链接"] = answers_url_list
data["作者姓名"] = authorName_list
data['作者id'] = authorid_list


data["关注者数量"] = Followers_number_final
data["浏览数量"] = Browsed_number_final
data["问题链接"] = problem_url
data["问题ID"] = problem_id[0]
data["问题标题"] = problem_title[0]
data["问题点赞数"] = problem_endorse[0]
data["问题评论数"] = problem_Comment[0]
data["问题回答数"] = answer_number[0]
data["问题标签"] = "&".join(problem_tags_list)
