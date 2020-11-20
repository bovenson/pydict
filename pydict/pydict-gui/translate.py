import urllib.request
import urllib.parse
import json
import pickle
import os.path
# 有道词典请求头部信息
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

languages = ('中文', '英语', '俄语', '日语', '西班牙语', '韩语')
language_map = {'ZH_CN':'中文', 'EN':'英语', 'RU':'俄语', 'JA':'日语', 'SP':'西班牙语', 'KR':'韩语'}
language_map_reverse = {'中文':'ZH_CN', '英语':'EN', '俄语':'RU', '日语':'JA', '西班牙语':'sp', '韩语':'KR'}

def formart_content(content):
    '''
    格式化要查询的文本
    去除开头结尾空字符;连续的空字符缩为一个空符
    '''
    return  ' '.join(filter(lambda x:x, content.split()))

class DataStructure:
    def __init__(self, lang1='none', lang2='none', trans='无法完成操作,是否无法连接网络?', trans_source='none'):
        self.lang1 = lang1
        self.lang2 = lang2
        self.trans = trans
        self.trans_source = trans_source
        pass

class Translate:
    '''
    翻译模块
    '''
    def __init__(self):
        self.count= 0
        self.trans_source = ''
        self.offline_data = {}
        self.save_data_limit_count = 5
        self.load_offline_data()
        pass
    def translate(self, content=' ', type='auto'):
        '''翻译'''
        data['type'] = type
        content = formart_content(content)
        if len(content)==0:
            print('没有输入内容')
            res = DataStructure()
            res.trans = '没有输入内容'
            return res
        # 自动离线查询结果
        if content not in self.offline_data:
            self.count += 1
            if (self.count >= self.save_data_limit_count):
                self.save_offline_data_to_file()
                self.count = 0
                pass
            pass
        #在线查询
        res = self.online_trans(content)
        if res == None:
            if content in self.offline_data.keys():
                res = self.offline_data[content]
                res.trans_source = '离线查询结果'
            else:
                res = DataStructure()
        if res == None:
            res = DataStructure()
        print('完成一次查询:' + res.lang1 + '--->' + res.lang2 + ' 结果:' + res.trans)
        return res
    def load_offline_data(self):
        '''
        从本地加载查询结果
        '''
        if os.path.exists('offline_data'):
            print('正在从本地加载查询结果...')
            try:
                with open('offline_data', 'rb') as pickle_file:
                    self.offline_data = pickle.load(pickle_file)
                print('从本地加载', len(self.offline_data), '条数据')
            except BaseException as reason:
                print('读取离线文件时遇到未知错误:',reason, '\n')
        pass
    def save_offline_data_to_file(self):
        '''
        将查询结果保存到本地
        '''
        print('正在保存查询结果到本地...')
        try:
            with open('offline_data', 'wb') as pickle_file:
                pickle.dump(self.offline_data, pickle_file)
        except BaseException as reason:
            print('保存离线文件时遇到未知错误:', reason)
        pass
    def online_trans(self, content):
        '''在线查询'''
        res = None
        try:
            data['i'] = content
            urldata = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request(url, urldata, head)
            response = urllib.request.urlopen(req, timeout=2)
            html = response.read().decode('utf-8')
            target = json.loads(html)
            #得到查询结果
            langs = target['type'].split('2', 1)
            trans = target['translateResult'][0][0]['tgt']
            res = DataStructure(language_map[langs[0]], language_map[langs[1]], trans, trans_source='在线查询结果')
            self.offline_data[content] = res
        except (OSError,urllib.error.URLError,urllib.error.URLError):
            res = None
        finally:
            return res
        pass
    def __del__(self):
        self.save_offline_data_to_file()
        pass