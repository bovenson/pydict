#!/usr/bin/python3
from tkinter_funs_bovenson import *
import turtle
import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    def createWidgets(self):
        pass

#创建应用
root = tk.Tk()
app = App(master=root)

#属性
screen_width = root.maxsize()[0]
screen_height = root.maxsize()[1]
app_width = int(screen_width*2/3)
app_height = int(screen_height*2/3)

#设置窗口属性
app.master.title("pydict")
app.master.resizable(False, False)
#设置窗口大小
app.master.geometry('%dx%d' % (app_width, app_height))
center_window(root, app_width, app_height)
#app.master.maxsize(app_width, app_height)

#运行窗口程序
app.mainloop()
