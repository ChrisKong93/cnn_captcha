# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import logging
import os
import random
import threading
import time

import wx
import wx.xrc
from PIL import Image
from recognize_local import main
from webserver_recognize_api import run


# from recognize_online import main


###########################################################################
## Class Frame
###########################################################################

class Frame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"This is Test Program", pos=wx.DefaultPosition,
                          size=wx.Size(600, 400), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.localpath = os.getcwd() + '/sample/test'
        files = ''
        for root, dirs, files in os.walk(self.localpath):
            pass
        L = len(files)
        print(L)
        if L == 0:
            return
        i = random.randint(0, L)
        # print(files[i])
        randompath = self.localpath + '/' + files[i]

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, randompath,
                                       wx.DefaultPosition, wx.Size(450, 35), 0)
        gSizer1.Add(self.m_textCtrl1, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"识别", wx.DefaultPosition, wx.Size(100, 35), 0)
        self.m_button1.SetDefault()
        gSizer1.Add(self.m_button1, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        bSizer1.Add(gSizer1, 1, wx.EXPAND, 5)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(560, 300), 0)
        self.m_staticText1.Wrap(-1)
        bSizer1.Add(self.m_staticText1, 0, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.click)

    def __del__(self):
        pass

    def click(self, event):
        event.Skip()
        path = self.m_textCtrl1.GetValue()
        print(path)
        logging.info(path)
        if self.checkimage(path) == 0:
            print('这个文件不存在')
            self.m_staticText1.SetLabel('这个文件不存在')
        else:
            self.m_staticText1.SetLabel(main(path))

    def checkimage(self, imagepath):
        size = (100, 60)
        if not os.path.exists(imagepath):
            return 0
        else:
            img = Image.open(imagepath)
            if img.size != size:
                img = img.resize(size, Image.ANTIALIAS)
            if img.format != 'PNG':
                imagepath = imagepath.split('.')[0] + '.png'
            img.save(imagepath)
            return 1


def kill_port(port):
    # 查找端口的pid
    find_port = 'netstat -aon | findstr %s' % port
    # print(find_port)
    print('正在检测端口是否被占用')
    logging.info('正在检测端口是否被占用')
    result = os.popen(find_port)
    text = result.read()
    result.close()
    if text != '':
        print(text)
        logging.info(text)
        print('端口被占用')
        logging.info('端口被占用')
        pid = text[-5:-1]
        print('占用端口的pid:' + pid)
        logging.info('占用端口的pid:' + pid)
        # 占用端口的pid
        find_kill = 'taskkill -f -pid %s' % pid
        # print(find_kill)
        result = os.popen(find_kill)
        result.close()
        print('端口已关闭')
        logging.info('端口已关闭')
        # return result.read()
        # print(result.read())
        # logging.info(result.read())
    else:
        print('端口未被占用')
        logging.info('端口未被占用')


def fun1():
    kill_port(6000)
    # os.system("python ./recognize_api.py")
    # os.system("recognize_api.exe") # 打包需要用这个命令
    run()


def runGUI():
    app = wx.App(False)
    frame = Frame(None)
    frame.Show(True)
    # start the applications
    app.MainLoop()


threads = []
threads.append(threading.Thread(target=fun1))
# threads.append(threading.Thread(target=runGUI))
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"  # 日志格式化输出
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"  # 日期格式
fp = logging.FileHandler('./log.txt', encoding='utf-8')
fs = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp])  # 调用
# logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, filename='./log.txt', filemode='w')

if __name__ == '__main__':
    # fun1()

    try:
        for t in threads:
            t.start()
            t.daemon()
        # print(threads[1].isAlive())
    except Exception as e:
        print(e)
        logging.warning(e)
    time.sleep(5)
    print(' * Running on http://127.0.0.1:{}/'.format(6000))
    runGUI()
    # while True:
    #     print(time.time())
    #     if threads[1].isAlive() == False:
    #         threads[0].join()
