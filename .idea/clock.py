'''
                                        Author:xtncsg（想听你唱首歌）
                                        create；2019-04-18
                                        update；2019-04-19
                                        bug:输入闹钟时间的时候，不能直接把输入框里面的数字全都删除
                                        unknown:ctypes 蜂鸣器
                                                StringVar()绑定变量
                                                局部函数里使用全局变量要global说明
                                                massagebox弹窗的自动关闭
                                                好像没有 RGB(255,255,255)这样生成颜色的宏
                                                同一个标签变量，不能两次放置，只会显示一次
                                                bind() 事件处理的绑定
                                                root.quit 和 root.destroy 的区别
'''

# from tkinter import*   并不鼓励使用from Tkinter import * 说是失去命名空间同时导致名字冲突
import tkinter
from datetime import datetime
import tkinter.messagebox as ms
import time
from threading import Thread
import  ctypes    # 关于系统蜂鸣器的库
player = ctypes.windll.kernel32  # 都是字母 l

# 生成全局窗口
root = tkinter.Tk()
root.title("闹钟定制")
# root.minsize(width = 800,height = 640)
root.geometry("1000x580") # 还可以继续缩小的窗口,中间是英文 x
# root.resizable(width = 1,height = 0)    设置窗口是否可以改变大小

game = tkinter.Label(root,text = "设置好闹钟时间后，若显示为ON则闹钟已经成功开启",height = 5,width = 50,bg = "#33FF00",fg = "#FF0000",font = 6)
game.place(x = 320,y = 5)


'''    必须要先生成窗口，才能绑定变量，因为StringVar 这个类里面，有一个成员函数 __init__(self, master=None, value=None, name=None)，
它的参数MASTER can be given as master widget.    '''

# 获取当前时间
# print(type(datetime.now()))  <class 'datetime.datetime'>
current_hour = datetime.now().hour
current_minute = datetime.now().minute
current_second = datetime.now().second
# print(type(curent_hour))  <class 'int'>


# 能自动刷新的字符串变量，可用set和get方法进行传值和取值
now_hour = tkinter.StringVar(value = current_hour)
now_minute = tkinter.StringVar(value = current_minute)
now_second = tkinter.StringVar(value = current_second)
# print(now_hour)         PY_VAR0
# print(type(now_hour))   <class 'tkinter.StringVar'>

clock_flag = False

# 与按键 ON/OFF 绑定的启动闹钟函数
def boot_clock():
    # global 说明这里的变量与外面的全局变量是一样的
    global clock_flag  #  local variable 'clock_flag' referenced before assignment
    clock_flag = not clock_flag

    clock_hour = int(hour_entry.get())  # 获取输入框里面的时间
    clock_minute = int(minute_entry.get())
    clock_second = int(second_entry.get())
    # print(type(clock_hour))  <class 'str'>

    if(clock_hour >= 24 or clock_minute >= 60 or clock_second >=60):
        ms.showerror("错误","闹钟时间设置错误\n请重新设置")
        # sys.exit(0)  这样整个程序就退出了，还是用 else 吧
    else:
         if(clock_flag):
            ms.showinfo("闹钟已经开启","闹钟将在{}时{}分{}秒时启动\n请注意躲避".format(clock_hour,clock_minute,clock_second))
            # showinfo(),showerror(),showwarning()
            confirm["text"] = "ON"
         else:
            confirm["text"] = "OFF"

# 响铃函数
def ring():
    for i in range(10):
        player.Beep(2000,1000)  # 频率和毫秒

# 时间匹配时，闹钟开始运行
def clock_start():
    Thread(target = ring).start()
    ms.showwarning("闹钟进行","闹钟开始了，大家快跑啊")
# 这里创建线程，要不然弹窗不关闭，就不会响铃

def timer():
    while(1):
        hour_num = int(now_hour.get()) # 获取当前时间
        minute_num = int(now_minute.get())
        second_num = int(now_second.get())
        # print(type(hour_num))  <class 'str'>

        # 非纯数字组成的字符串强转为整型会报错：ValueError: invalid literal for int() with base 10
        # 所以在输入框输入数字的时候，不能一下子把原来的数字都删掉，这样就变成空字符串了
        clock_hour = int(hour_entry.get())  # 获取输入框里面的时间
        clock_minute = int(minute_entry.get())
        clock_second = int(second_entry.get())
        # print(type(clock_hour))  <class 'str'>

        second_num += 1
        if second_num == 60:
            minute_num +=1
            second_num = 0
            if minute_num == 60:
                hour_num += 1
                minute_num =0
                if hour_num == 24:
                    hour_num = 0
        now_hour.set("%02d"%hour_num)  # 指定格式更新数据
        now_minute.set("%02d"%minute_num)
        now_second.set("%02d"%second_num)

        if(clock_flag == True and hour_num == clock_hour and minute_num == clock_minute and second_num == clock_second):
            Thread(target = clock_start).start()
        # 这里创建线程，要不然闹钟开始的时候，时钟就不走了
        # 时间每隔一秒刷新一次
        time.sleep(1)   # 单位是秒

if __name__ == '__main__':
    # 用 RGB 生成颜色
    # current_time = tkinter.Label(root,width = 10,height = 1,text = "现在时间：",font = 3,bg = RGB(20,184,152))

    # "#33FF00"十六进制表示的颜色字符串，R,G,B各占一个字节
    current_time = tkinter.Label(root,width = 10,height = 1,text = "现在时间：",font = 3,bg = "#33FF00",fg = "#FF3333")
    current_time.place(x = 10,y = 5)

    current_time_hour = tkinter.Label(root,width = 2,height = 1,textvariable = now_hour,font = 3,bg = "#3333FF",fg = "#FF3333")
    current_time_hour.place(x = 140,y = 5)

    tmp_1 = tkinter.Label(root,width = 1,height = 1,text = ":",font = 1)
    tmp_1.place(x = 165,y = 5)

    current_time_minute = tkinter.Label(root,width = 2,height = 1,textvariable = now_minute,font = 3,bg = "#3333FF",fg = "#FF3333")
    current_time_minute.place(x = 190,y = 5)

    # 必须要生成两个临时标签，要不然只会放置一次
    tmp_2 = tkinter.Label(root,width = 1,height = 1,text = ":",font = 1)
    tmp_2.place(x = 215,y = 5)

    current_time_second = tkinter.Label(root,width = 2,height = 1,textvariable = now_second,font = 3,bg = "#3333FF",fg = "#FF3333")
    current_time_second.place(x = 240,y = 5)

    clock_set = tkinter.Label(root,width = 10,height = 1,text = "设置闹钟：",font = 3,bg = "#FFFF00",fg = "#FF3333")
    clock_set.place(x = 10,y = 80)

    '''Entry 窗口是没有 height 属性的
    Entry等控件中的参数是关键字参数，其由键-值组成。关键字参数是在传递构成中不必按照顺序传递
    必须要提供”传递参数名=传递参数值”形式的参数，而传递过程中也转变为dict的键值对map关系。
    参数里面的 root 是 master，entry 控件的父控件，也就是放置 entry 的控件 '''

    hour_entry = tkinter.Entry(root,width = 2,font = 3,bg = "#66CC33",fg = "#FF3333")   # show = '*'
    hour_entry.place(x = 140,y = 80)

    tmp_3 = tkinter.Label(root,width = 1,height = 1,text = ":",font = 1)
    tmp_3.place(x = 165,y = 80)

    minute_entry = tkinter.Entry(root,width = 2,font = 3,bg = "#66CC33",fg = "#FF3333")
    minute_entry.place(x = 190,y = 80)

    tmp_4 = tkinter.Label(root,width = 1,height = 1,text = ":",font = 1)
    tmp_4.place(x = 215,y = 80)

    second_entry = tkinter.Entry(root,width = 2,font = 3,bg = "#66CC33",fg = "#FF3333")
    second_entry.place(x = 240,y = 80)

    hour_entry.insert("end","00")  # 必须要指明插入的位置
    minute_entry.insert("end","00")
    second_entry.insert("end","00")

    # command 绑定事件好像只能鼠标左键单击,command 绑定的是一个回调函数
    confirm = tkinter.Button(root,font = 3,bg = "#66CC33",fg= "#FF3300",height = 1,width = 10,activebackground = "#0000FF",text = "OFF",command = boot_clock)
    confirm.place(x = 400,y = 200)

    quit = tkinter.Button(root,font = 3,bg = "#66CC33",fg= "#FF3300",height = 1,width = 10,activeforeground = "#0000FF",text = "退出程序",command = root.destroy)
    # root.destroy 会很快关闭，root.quit 关闭的就很慢
    quit.place(x = 400,y = 300)

    '''confirm.bind( "<Button-1>",start()) 如果不加括号的话，start() takes 0 positional arguments but 1 was given
    用bind() 绑定的时候，没有发生事件也会自动调用 start() 函数
    回调函数与函数：fun与fun（） 作为参数时表示的意义不同，fun作为参数表示是函数，fun（）作为参数时表示一个值 '''

    clock_t = Thread(target = timer)   # 创建线程的时候，这里不能有括号
    clock_t.start()
    # 启动主窗口消息循环
    root.mainloop()
