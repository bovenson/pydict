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
        #设置窗口属性
        self.master.title("pydict")
        self.master.resizable(False, False)

        #添加组件
        self.label_origin_tip = tk.Label(root, text='输入要翻译的文本:')
        self.label_origin_tip.grid(row=0, column=0, columnspan=4, sticky='W')

        self.label_transtype_text = tk.StringVar()
        self.label_transtype = tk.Label(root, textvariable=self.label_transtype_text)
        self.label_transtype.grid(row=0, column=4, columnspan=4, sticky='W')

        self.label_trans_tip = tk.Label(root, text='翻译结果')
        self.label_trans_tip.grid(row=0, column=4, columnspan=4, sticky='E')
        
        self.text_origin = tk.Text(root, width=60)
        self.text_origin.grid(row=1, column=0, columnspan=4)
        self.text_trans = tk.Text(root, width=60)
        self.text_trans.grid(row=1, column=4, columnspan=4)

        #语言选择
        self.label_lang_choice = tk.Label(root, text='源语言:')
        self.label_lang_choice.grid(row=2, column=0, sticky='E')

        self.variable_lang1 = tk.StringVar()
        self.variable_lang1.set("中文")

        self.optionmenu_lang1 = tk.OptionMenu(root, self.variable_lang1, '中文', '英语', '俄语', '日语', '西班牙语', '韩语')
        self.optionmenu_lang1.grid(row=2, column=1, sticky='W')

        self.label_lang_to = tk.Label(root, text='目标语言:')
        self.label_lang_to.grid(row=2, column=2, sticky='E')

        self.variable_lang2 = tk.StringVar()
        self.variable_lang2.set("英语")

        self.optionmenu_lang2 = tk.OptionMenu(root, self.variable_lang2, '中文', '英语', '俄语', '日语', '西班牙语', '韩语')
        self.optionmenu_lang2.grid(row=2, column=3, sticky='W')

        #翻译按钮
        self.button_ok2trans_select = tk.Button(root, text=' 选择翻译 ', command=self.select_translate)
        self.button_ok2trans_select.grid(row=2, column=5)
        #翻译按钮
        self.button_ok2trans_auto = tk.Button(root, text=' 自动翻译 ', command=self.auto_translate)
        self.button_ok2trans_auto.grid(row=2, column=6)

        pass
    def update_text_trans(self, text):
        self.text_trans.state=tk.NORMAL
        self.text_trans.delete(0.0, tk.END)
        self.text_trans.insert(tk.INSERT, text)
        self.text_trans.state=tk.DISABLED
        pass
    def select_translate(self):
        lang1 = language_map_reverse[self.variable_lang1.get()]
        lang2 = language_map_reverse[self.variable_lang2.get()]
        type = lang1 + '2' + lang2
        if lang1=='ZH_CN' or lang2=='ZH_CN':
            self.auto_translate(type=type)
        else:
            content = self.text_origin.get(0.0, tk.END)
            res = self.cls_trans.translate(content=content, type=lang1+'2ZH_CN')
            self.auto_translate(content=res.trans, type='ZH_CN2'+lang2)
        #print(language_map_reverse[self.variable_lang1.get()], language_map_reverse[self.variable_lang2.get()])
        #print(self.variable_lang2.get())
        pass
    def auto_translate(self, content=None, type='auto'):
        if content == None:
            content = self.text_origin.get(0.0, tk.END)
        res = self.cls_trans.translate(content=content, type=type)
        trans = res.trans
        self.update_text_trans(trans)
        self.label_transtype_text.set('翻译类型: ' + res.lang1 + ' --> ' + res.lang2 + '    来源:' + res.trans_source)
        pass
    def createWidgets(self):
        pass
#    def __del__(self):
#        self.cls_trans.save_offline_data_to_file()
#        pass

#创建应用
root = tk.Tk()

#设置窗口大小
#属性
#screen_width = root.maxsize()[0]
#screen_height = root.maxsize()[1]
#app_width = int(screen_width*2/3)
#app_height = int(screen_height*2/3)
#root.geometry('%dx%d' % (app_width, app_height))
#center_window(root, app_width, app_height)

app = App(master=root)


#运行窗口程序
app.mainloop()
