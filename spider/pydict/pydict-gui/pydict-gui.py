#!/usr/bin/python3
# coding:utf-8
from tkinter_funs_bovenson import *
from translate import *
import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.init()
        self.createWidgets()
        self.grid()

        self.cls_trans = Translate()
        pass
    def init(self):
        #属性
        self.screen_width = root.maxsize()[0]
        self.screen_height = root.maxsize()[1]
        self.app_width = int(self.screen_width*2/3)
        self.app_height = int(self.screen_height*2/3)

        #设置窗口属性
        self.master.title("pydict")
        self.master.resizable(False, False)

        #设置窗口大小
        #self.master.geometry('%dx%d' % (self.app_width, self.app_height))
        #center_window(self.master, self.app_width, self.app_height)

        #添加组件
        self.label_origin_tip = tk.Label(root, text='输入要翻译的文本:')
        self.label_origin_tip.grid(row=0, column=0, sticky=tk.W)

        self.label_transtype_text = tk.StringVar()
        self.label_transtype = tk.Label(root, textvariable=self.label_transtype_text)
        self.label_transtype.grid(row=0, column=1, sticky=tk.W)

        self.label_trans_tip = tk.Label(root, text=':翻译结果')
        self.label_trans_tip.grid(row=0, column=1, sticky='E')
        
        self.text_origin = tk.Text(root)
        self.text_origin.grid(row=1, column=0)
        self.text_trans = tk.Text(root)
        self.text_trans.grid(row=1, column=1)

        self.button_ok2trans = tk.Button(root, text='翻译', command=self.translate)
        self.button_ok2trans.grid(row=2, columnspan=2)

        pass
    def update_text_trans(self, text):
        self.text_trans.state=tk.NORMAL
        self.text_trans.delete(0.0, tk.END)
        self.text_trans.insert(tk.INSERT, text)
        self.text_trans.state=tk.DISABLED
        pass
    def translate(self):
        content = self.text_origin.get(0.0, tk.END)
        res = self.cls_trans.translate(content)
        trans = res.trans
        self.update_text_trans(trans)
        self.label_transtype_text.set('翻译类型: ' + res.lang1 + ' --> ' + res.lang2 + '    来源:' + res.trans_source)
        pass
    def createWidgets(self):
        pass
    def __del__(self):
        self.cls_trans.save_offline_data_to_file()
        pass

#创建应用
root = tk.Tk()
app = App(master=root)
#运行窗口程序
app.mainloop()
