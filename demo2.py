# -*- coding=utf-8 -*
# 中文显示乱码

from tkinter import *

# 第一部分
# 创建界面
root = Tk()
root.title('网易云音乐')  # add title
root.geometry('560x450')  # set window size

# 标签控件
label = Label(root, text='请输入下载歌曲： ', font=('华文行楷', 20))
# 标签定位
label.grid()  # 默认 row=0, col=0
# 输入框
entry = Entry(root, font=('SimHei', 20))
entry.grid(row=0, column=1)

root.mainloop()  # 显示界面
