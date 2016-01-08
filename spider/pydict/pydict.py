#!/usr/bin/python3
__author__ = '孙振凯'
import urllib.request
import urllib.parse
import json
import pickle
import os.path

language_map = {'ZH_CN':'中文', 'EN':'英语', 'RU':'俄语', 'JA':'日语', 'SP':'西班牙语', 'KR':'韩语'}
class OfflineData:
    def __init__(self, lang1, lang2, trans):
        self.lang1 = lang1
        self.lang2 = lang2
        self.trans = trans

#请求头部信息
head = {}
head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'
# 有道词典POST的数据内容
url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=http://www.youdao.com/'
data = {}
data['type'] = 'auto'
data['i'] = ""
data['doctype'] = 'json'
data['xmlVersion'] = '1.8'
data['keyfrom'] = 'fanyi.web'
data['ue'] = 'UTF-8'
data['action'] = 'FY_BY_CLICKBUTTON'
data['typoResult'] = 'true'

again = ''
offline_data = {}
count = 0
count_limit_to_save = 30

def load_offline_data():
    '''
    从本地加载查询结果
    '''
    global offline_data
    if os.path.exists('offline_data'):
        print('正在从本地加载查询结果...')
        try:
            with open('offline_data', 'rb') as pickle_file:
                offline_data = pickle.load(pickle_file)
            print('从本地加载', len(offline_data), '条数据')
        except BaseException as reason:
            print('读取离线文件时遇到未知错误:',reason, '\n')
    pass

def save_offline_data_to_file():
    '''
    将查询结果保存到本地
    '''
    global offline_data
    print('正在保存查询结果到本地...')
    try:
        with open('offline_data', 'wb') as pickle_file:
            pickle.dump(offline_data, pickle_file)
    except BaseException as reason:
        print('保存离线文件时遇到未知错误:', reason)
    pass

def formart_content(content):
    '''
    格式化要查询的文本
    去除开头结尾空字符;连续的空字符缩为一个空符
    '''
    return  ' '.join(filter(lambda x:x, content.split()))

def print_answer(lang1, lang2, trans):
    '''
    打印结果
    '''
    try:
        print('翻译类型:', language_map[lang1], '-->', language_map[lang2])
    except KeyError:
        print('未知语言类型')
    print('翻译结果:', trans, '\n')

def print_offline_data(content):
    '''
    查找离线翻译
    '''
    print('显示离线结果')
    res = offline_data[content]
    print_answer(res.lang1, res.lang2, res.trans)

def save_offline_data(content, lang1, lang2, trans):
    '''
    保存离线结果
    '''
    ans = OfflineData(lang1, lang2, trans)
    offline_data[content] = ans
    pass

def translate(content):
    '''
    在线翻译
    '''
    global offline_data
    global count
    #处理查询结果到达一定数量后自动保存
    if content not in offline_data.keys():
        count += 1
    if count >= count_limit_to_save:
        save_offline_data_to_file()
        count = 0
    data['i'] = content
    urldata = urllib.parse.urlencode(data).encode('utf-8')

    #在线查询
    req = urllib.request.Request(url, urldata, head)
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    target = json.loads(html)
    #得到查询结果
    langs = target['type'].split('2', 1)
    trans = target['translateResult'][0][0]['tgt']
    #打印结果
    print_answer(langs[0], langs[1], trans)
    #保存查询结果
    save_offline_data(content, langs[0], langs[1], trans)
    #offline_data[content] = langs[0] + ':::' + langs[1] + ':::' + target['translateResult'][0][0]['tgt']


########################################################################33
#主程序开始
#开始&预备
print('欢迎使用在线翻译工具\n支持的语言:')
for each in language_map.values():
    print(each,end=' ')
print('\nPowered by youdao')
print('Bug report:szhkai@126.com')
load_offline_data()

print('*********************************************\n')

while True:
    try:
        if again=='n' or again=='N':
            break
        if len(again)>0:
            content = again
        else:
            content = input('输入需要翻译的内容:')
        #格式化要翻译内容
        content = formart_content(content)
        if len(content)==0:
            print('不要什么也不让我翻译')
            again = input('继续翻译?(退出请输入n/N,回车继续)')
            continue
        translate(content)
        again = input('继续翻译?(退出请输入n/N,回车继续)')
    except (OSError,urllib.error.URLError):
        if content in offline_data.keys():
            print_offline_data(content)
        else:
            print('网络错误,请联网后重试...\n')
        again = ''
    except:
        print('未知错误,请重试\n')
        again = ''

save_offline_data_to_file()
