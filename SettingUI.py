#coding:utf-8
import os
import  wx
import  LogOutput as LoadLog
import idDefine as gen

class SettingPanel(wx.Listbook):
    def __init__(self,parent,confdict):
        wx.Listbook.__init__(self, parent, wx.ID_ANY, style=wx.BK_DEFAULT)
        self.LogLevelList = ['debug','info','warning','error','critical']
        self.confdict = confdict
        self.GetConfigDictValue(self.confdict)

        pages = [(self.BaseSettingUI(), u" 基本设置          "),
                 (self.ProMonUI(),      u" 进程监控          "),
                 (self.sysInfoUI(),     u" 系统资源          "),
                 (self.LogSettingUI(),  u" 日志配置          "),]
        imID = 0
        for page, label in pages:
            self.AddPage(page, label, imageId=imID)
            imID += 1

        # self.Bind(wx.EVT_TREEBOOK_PAGE_CHANGED, self.OnPageChanged)
        # self.Bind(wx.EVT_TREEBOOK_PAGE_CHANGING, self.OnPageChanging)

        self.SetConfigDataOnUI()

    def BaseSettingUI(self):
        p = wx.Panel(self, -1)#子窗体的容器
        win=wx.Panel(p,-1)

        about_s = wx.StaticText(win,-1,u"基本设置")
        line = wx.StaticLine(win)
        self.startup_c = wx.CheckBox(win, label=u"随系统启动",id = gen.ID_STARTUP)
        self.startup_c.Disable()
        #print "bool self.startup: ",self.startup
        self.minicon_c = wx.CheckBox(win, label=u"最小化系统托盘",id = gen.ID_MINICON)
        self.minicon_c.Disable()
        self.checkupdate_c = wx.CheckBox(win, label=u"自动检测更新",id = gen.ID_AUTOUPDATE)
        self.checkupdate_c.Disable()
        self.defaultbtn = wx.Button(win,label=u"还原默认设置",size=(100,25),id=gen.ID_DEFAULT)

        sizer = wx.GridBagSizer(5,5)
        sizer.Add(about_s,pos=(0,0),span=(1,1),flag=wx.TOP|wx.LEFT, border=10)
        sizer.Add(line,pos=(1,0),span=(1,3),flag=wx.EXPAND|wx.RIGHT|wx.LEFT|wx.TOP,border=5)
        sizer.Add(self.startup_c,pos=(2,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(self.minicon_c,pos=(3,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(self.checkupdate_c,pos=(4,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(self.defaultbtn,pos=(5,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        sizer.AddGrowableCol(1,1)
        win.SetSizerAndFit(sizer)
        sizer.SetSizeHints(self)

        def OnCPSize(evt, win=win):
            win.SetPosition((0,0))
            win.SetSize(evt.GetSize())

        p.Bind(wx.EVT_SIZE, OnCPSize)
        # p.Bind(wx.EVT_CHECKBOX, self.OnBaseConfig, id=gen.ID_STARTUP)
        # p.Bind(wx.EVT_CHECKBOX, self.OnBaseConfig, id=gen.ID_MINICON)
        # p.Bind(wx.EVT_CHECKBOX, self.OnBaseConfig, id=gen.ID_AUTOUPDATE)
        p.Bind(wx.EVT_BUTTON, self.OnBaseConfig, id=gen.ID_DEFAULT)
        return p

    def OnBaseConfig(self,event):

            # defaultDlog = wx.MessageDialog(self,u"您确定要还原默认值吗？", u'确认提示',
            #                                    wx.YES_NO|wx.YES_NO)
            # if defaultDlog.ShowModal() == wx.ID_YES:
            #     f = HandleSetting(gen.CONF_FILE,gen.DEFAULT_CONFIG_DICT)
            #     f.WriteConfFile()
            # defaultDlog.Destroy()
        #gen.LoadDefaultConf = True
        self.GetConfigDictValue(gen.DEFAULT_CONFIG_DICT)
        #print  u"默认字典",gen.DEFAULT_CONFIG_DICT
        self.SetConfigDataOnUI()

    def ProMonUI(self):
        p = wx.Panel(self, -1)#子窗体的容器
        win=wx.Panel(p,-1)
        ##控件
        about_s = wx.StaticText(win,-1,u"监控设置")
        looptime_s = wx.StaticText(win,-1,u"检测进程运行状态的间隔时间：")
        self.looptime_t  = wx.TextCtrl(win,size=(100,20))
        looptime_s2 = wx.StaticText(win,-1,u"秒")
        datafile_s = wx.StaticText(win,-1,u"数据文件：")
        self.datafile_t = wx.TextCtrl(win,size=(100,20),style=wx.TE_READONLY)
        self.datafile_b = wx.Button(win,label=u"打开",size=(50,20),id=gen.ID_DATA)
        line = wx.StaticLine(win)
        ##布局
        sizer = wx.GridBagSizer(4,5)
        sizer.Add(about_s,pos=(0,0),span=(1,1),flag=wx.TOP|wx.LEFT, border=10)
        sizer.Add(line,pos=(1,0),span=(1,3),flag=wx.EXPAND|wx.RIGHT|wx.LEFT|wx.TOP,border=5)
        sizer.Add(looptime_s,pos=(2,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(self.looptime_t,pos=(2,1),span=(1,1),flag=wx.TOP|wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(looptime_s2,pos=(2,2),span=(1,1),flag=wx.TOP|wx.RIGHT, border=10)
        sizer.Add(datafile_s,pos=(3,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(self.datafile_t,pos=(3,1),span=(1,1),flag=wx.TOP|wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(self.datafile_b,pos=(3,2),span=(1,1),flag=wx.TOP|wx.RIGHT, border=10)
        sizer.AddGrowableCol(1,1)
        win.SetSizerAndFit(sizer)
        sizer.SetSizeHints(self)

        ##事件
        p.Bind(wx.EVT_BUTTON,self.OnOpenFile,id=gen.ID_DATA)
        ##设置值
        # self.looptime_t.SetValue(str(self.round_robin_scheduling))
        # self.datafile_t.SetValue(self.data_file)

        def OnCPSize(evt, win=win):
            win.SetPosition((0,0))
            win.SetSize(evt.GetSize())
        p.Bind(wx.EVT_SIZE, OnCPSize)
        return p


    def sysInfoUI(self):
        p = wx.Panel(self, -1)#子窗体的容器
        win=wx.Panel(p,-1)

        about_s = wx.StaticText(win,-1,u"系统资源")
        line = wx.StaticLine(win)
        self.cpu_c = wx.CheckBox(win, label=u"启用系统CPU监控",id=gen.ID_MONITOR_CPU)
        self.memory_c = wx.CheckBox(win, label=u"启用系统内存监控",id=gen.ID_MONITOR_MEMORY)
        loopTimeCpu_s = wx.StaticText(win,-1,u"监控CPU的间隔时间：")
        self.loopTimeCpu_t  = wx.TextCtrl(win,size=(100,20))

        loopTimeCpu_s2 = wx.StaticText(win,-1,u"(建议:30-180) 秒")
        loopTimeMemory_s = wx.StaticText(win,-1,u"监控内存的间隔时间：")
        self.loopTimeMemory_t  = wx.TextCtrl(win,size=(100,20))
        loopTimeMemory_s2 = wx.StaticText(win,-1,u"(建议:30-180) 秒")

        sizer = wx.GridBagSizer(5,5)
        sizer.Add(about_s,pos=(0,0),span=(1,1),flag=wx.TOP|wx.LEFT, border=10)
        sizer.Add(line,pos=(1,0),span=(1,3),flag=wx.EXPAND|wx.RIGHT|wx.LEFT|wx.TOP,border=5)
        sizer.Add(self.cpu_c,pos=(2,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(self.memory_c,pos=(3,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)

        sizer.Add(loopTimeCpu_s,pos=(4,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(self.loopTimeCpu_t,pos=(4,1),span=(1,1),flag=wx.TOP|wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(loopTimeCpu_s2,pos=(4,2),span=(1,1),flag=wx.TOP|wx.RIGHT, border=10)

        sizer.Add(loopTimeMemory_s,pos=(5,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(self.loopTimeMemory_t,pos=(5,1),span=(1,1),flag=wx.TOP|wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(loopTimeMemory_s2,pos=(5,2),span=(1,1),flag=wx.TOP|wx.RIGHT, border=10)
        sizer.AddGrowableCol(1,1)
        win.SetSizerAndFit(sizer)
        sizer.SetSizeHints(self)

        ##绑定事件
        self.Bind(wx.EVT_CHECKBOX,self.OnSysInfoCPU,id=gen.ID_MONITOR_CPU)
        self.Bind(wx.EVT_CHECKBOX,self.OnSysInfoMemory,id=gen.ID_MONITOR_MEMORY)
        ##设置值
        # self.cpu_c.SetValue(self.enable_monitor_cpu)
        # self.memory_c.SetValue(self.enable_monitor_memory)
        # self.loopTimeMemory_t.SetValue(str(self.memory_scheduling))
        # if self.memory_c.GetValue() is True:
        #     self.loopTimeMemory_t.Enable()
        # else:
        #     self.loopTimeMemory_t.Disable()
        #
        # self.loopTimeCpu_t.SetValue(str(self.cpu_scheduling))
        # if self.cpu_c.GetValue() is True:
        #     self.loopTimeCpu_t.Enable()
        # else:
        #     self.loopTimeCpu_t.Disable()

        def OnCPSize(evt, win=win):
            win.SetPosition((0,0))
            win.SetSize(evt.GetSize())
        p.Bind(wx.EVT_SIZE, OnCPSize)
        return p

    def OnSysInfoCPU(self,event):
        if event.IsChecked():
            self.loopTimeCpu_t.Enable()
        else:
            self.loopTimeCpu_t.Disable()

    def OnSysInfoMemory(self,event):
        if event.IsChecked():
            self.loopTimeMemory_t.Enable()
        else:
            self.loopTimeMemory_t.Disable()

    def LogSettingUI(self):
        p = wx.Panel(self, -1)#子窗体的容器
        win=wx.Panel(p,-1)

        about_s = wx.StaticText(win,-1,u"日志配置")
        line = wx.StaticLine(win)
        print "self.enable_console_show:",self.enable_console_show
        self.enableconsole_c = wx.CheckBox(win, label=u"启用控制台信息输出 (依赖于文件日志)",id=gen.ID_CONSOLE_SHOW)
        self.enablelog_c = wx.CheckBox(win, label=u"启用文件日志输出",id=gen.ID_LOG_SHOW)

        logfile_s = wx.StaticText(win,-1,u"日志文件：")
        self.logfile_t  = wx.TextCtrl(win,size=(238,20),style=wx.TE_READONLY)
        logfile_s2 = wx.Button(win,label=u"打开",size=(50,20),id=gen.ID_LOG_FILE)

        logkeep_s = wx.StaticText(win,-1,u"日志保留：")
        self.logkeep_t  = wx.TextCtrl(win,size=(80,20))
        logkeep_s2 = wx.StaticText(win,-1,u"份")

        logsize_s = wx.StaticText(win,-1,u"日志大小：")
        self.logsize_t  = wx.TextCtrl(win,size=(80,20))
        logsize_s2 = wx.StaticText(win,-1,u"M")

        clear_clog_s = wx.StaticText(win,-1,u"当超过")
        self.clear_clog_t  = wx.TextCtrl(win,size=(70,20))
        clear_clog_s2 = wx.StaticText(win,-1,u"字节时，自动清空控制台内容")

        self.consolelevel_r = wx.RadioBox(win, -1, u"控制台日志级别", (10,10), wx.DefaultSize, self.LogLevelList, 2, wx.RA_SPECIFY_COLS)
        self.loglevel_r = wx.RadioBox(win, -1, u"文件输出日志级别", (10,10), wx.DefaultSize, self.LogLevelList, 2, wx.RA_SPECIFY_COLS)

        sizer = wx.GridBagSizer(9,6)
        sizer.Add(about_s,pos=(0,0),span=(1,1),flag=wx.TOP|wx.LEFT, border=10)
        sizer.Add(line,pos=(1,0),span=(1,5),flag=wx.EXPAND|wx.RIGHT|wx.LEFT|wx.TOP,border=5)

        sizer.Add(self.enablelog_c,pos=(2,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(self.enableconsole_c,pos=(2,1),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)

        blsizer = wx.BoxSizer(wx.HORIZONTAL)
        blsizer.Add(logfile_s,0, wx.ALL, 0)
        blsizer.Add(self.logfile_t,0, wx.ALL, 0)
        blsizer.Add(logfile_s2,0, wx.LEFT, 5)
        sizer.Add(blsizer,pos=(3,0),span=(1,5),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)

        # sizer.Add(logkeep_s,pos=(4,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        # sizer.Add(logkeep_t,pos=(4,1),span=(1,1),flag=wx.TOP|wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border=10)
        # sizer.Add(logkeep_s2,pos=(4,2),span=(1,1),flag=wx.TOP|wx.RIGHT, border=10)

        bsizer = wx.BoxSizer(wx.HORIZONTAL)
        bsizer.Add(logkeep_s, 0, wx.ALL, 0)
        bsizer.Add(self.logkeep_t, 0, wx.ALL, 0)
        bsizer.Add(logkeep_s2, 0, wx.LEFT, 5)

        bsizer.Add(logsize_s, 0, wx.LEFT, 40)
        bsizer.Add(self.logsize_t, 0, wx.ALL, 0)
        bsizer.Add(logsize_s2, 0, wx.LEFT, 5)
        sizer.Add(bsizer,pos=(4,0),span=(1,5),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)

        clearsizer = wx.BoxSizer(wx.HORIZONTAL)
        clearsizer.Add(clear_clog_s,0, wx.ALL, 0)
        clearsizer.Add(self.clear_clog_t,0, wx.LEFT, 5)
        clearsizer.Add(clear_clog_s2,0, wx.LEFT, 5)
        sizer.Add(clearsizer,pos=(5,0),span=(1,5),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)

        sizer.Add(self.consolelevel_r,pos=(6,0),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        sizer.Add(self.loglevel_r,pos=(6,1),span=(1,1),flag=wx.TOP|wx.LEFT|wx.EXPAND, border=10)
        #sizer.AddGrowableCol(1,1)
        win.SetSizerAndFit(sizer)
        sizer.SetSizeHints(self)

        ##设置值
        # self.enablelog_c.SetValue(self.enable_log)
        # if self.enable_console_show is True:
        #     self.enableconsole_c.SetValue(True)
        #     self.enablelog_c.SetValue(True)
        # if self.enable_log is False:
        #     self.enableconsole_c.SetValue(False)
        #     self.enablelog_c.SetValue(False)
        # self.logfile_t.SetValue(self.log_file)
        # self.logkeep_t.SetValue(str(self.log_leave))
        # self.logsize_t.SetValue(str(self.log_size))
        # self.clear_clog_t.SetValue(str(gen.MSG_MAX))
        # self.consolelevel_r.SetSelection(self.console_level)
        # self.loglevel_r.SetSelection(self.log_level)

        def OnCPSize(evt, win=win):
            win.SetPosition((0,0))
            win.SetSize(evt.GetSize())
        p.Bind(wx.EVT_SIZE, OnCPSize)
        p.Bind(wx.EVT_CHECKBOX,self.OnEnableLog,id=gen.ID_CONSOLE_SHOW)
        p.Bind(wx.EVT_CHECKBOX,self.OnEnableLog2,id=gen.ID_LOG_SHOW)
        p.Bind(wx.EVT_BUTTON,self.OnOpenFile,id=gen.ID_LOG_FILE)

        return p

    def OnEnableLog(self,event):
        if event.IsChecked:
            self.enablelog_c.SetValue(True)

    def OnEnableLog2(self,event):
        if event.IsChecked:
            self.enableconsole_c.SetValue(False)

    # def OnPageChanged(self, event):
    #     old = event.GetOldSelection()
    #     new = event.GetSelection()
    #     sel = self.GetSelection()
    #     #print 'OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel)
    #     event.Skip()
    #
    # def OnPageChanging(self, event):
    #     old = event.GetOldSelection()
    #     new = event.GetSelection()
    #     sel = self.GetSelection()
    #     #print 'OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel)
    #     event.Skip()

    def OnOpenFile(self,evnet):
        #LoadLog.LogMsg(gen.logger.info,u"打开数据文件")
        if evnet.GetId() == gen.ID_DATA:
            wildcard = "Json File (*.json)|*.json|" \
                   "All files (*.*)|*.*"
            ctrltext = self.datafile_t
        else:
            wildcard = "Log File (*.log)|*.log|" \
                       "Docuement File (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"
            ctrltext = self.logfile_t

        OpenDlg = wx.FileDialog(self, u"选择文件",os.getcwd(), "", wildcard, wx.OPEN)
        if OpenDlg.ShowModal() == wx.ID_OK:
            ctrltext.SetValue(OpenDlg.GetPath())
            LoadLog.LogMsg(gen.logger.info,u"打开文件对话框所更换的文件: %s" % OpenDlg.GetPath())
        OpenDlg.Destroy()

    def SetConfigDataOnUI(self):
        ##基本设置的设定值
        self.startup_c.SetValue(self.startup)
        self.minicon_c.SetValue(self.tray_minimize)
        self.checkupdate_c.SetValue(self.autoupdate)

        ##进程监控的设定值
        self.looptime_t.SetValue(str(self.round_robin_scheduling))
        self.datafile_t.SetValue(self.data_file)

        ##系统监控的设定值
        self.cpu_c.SetValue(self.enable_monitor_cpu)
        self.memory_c.SetValue(self.enable_monitor_memory)
        self.loopTimeMemory_t.SetValue(str(self.memory_scheduling))
        if self.memory_c.GetValue() is True:
            self.loopTimeMemory_t.Enable()
        else:
            self.loopTimeMemory_t.Disable()

        self.loopTimeCpu_t.SetValue(str(self.cpu_scheduling))
        if self.cpu_c.GetValue() is True:
            self.loopTimeCpu_t.Enable()
        else:
            self.loopTimeCpu_t.Disable()

        ##日志的设置值
        self.enablelog_c.SetValue(self.enable_log)
        if self.enable_console_show is True:
            self.enableconsole_c.SetValue(True)
            self.enablelog_c.SetValue(True)
        if self.enable_log is False:
            self.enableconsole_c.SetValue(False)
            self.enablelog_c.SetValue(False)
        self.logfile_t.SetValue(self.log_file)
        self.logkeep_t.SetValue(str(self.log_leave))
        self.logsize_t.SetValue(str(self.log_size))
        self.clear_clog_t.SetValue(str(gen.MSG_MAX))
        self.consolelevel_r.SetSelection(self.console_level)
        self.loglevel_r.SetSelection(self.log_level)


    def GetConfigDictValue(self,confdict):
        # print "startup: ",self.confdict["base"]["startup"]
        # print "type startup: ",type(self.confdict["base"]["startup"])

        if confdict["base"]["startup"] == True:
            self.startup = True
        else:
            self.startup = False

        if confdict["base"]["tray_minimize"] == True:
            self.tray_minimize = True
        else:
            self.tray_minimize = False

        if confdict["base"]["autoupdate"] == True:
            self.autoupdate = True
        else:
            self.autoupdate = False

        self.round_robin_scheduling = int(confdict["monitor"]["round_robin_scheduling"])

        self.data_file = confdict["monitor"]["data_file"]
        if os.path.abspath(self.data_file) is not True:
            self.data_file = os.path.join(os.getcwd(), self.data_file)

        self.enable_monitor_cpu = confdict["monitor"]["enable_monitor_cpu"]

        self.enable_monitor_memory = confdict["monitor"]["enable_monitor_memory"]

        self.cpu_scheduling = confdict["monitor"]["cpu_scheduling"]
        #print "self.cpu_sheduling:", self.cpu_scheduling, type(self.cpu_scheduling)

        self.memory_scheduling = confdict["monitor"]["memory_scheduling"]

        self.enable_console_show = confdict["log"]["enable_console_show"]
        self.enable_log = self.confdict["log"]["enable_log"]


        self.log_file = self.confdict["log"]["log_file"]
        if os.path.abspath(self.log_file) is not True:
            self.log_file = os.path.join(os.getcwd(),self.log_file)

        self.log_leave = confdict["log"]["log_leave"]
        self.log_size = confdict["log"]["log_size"]

        self.msg_max = confdict["log"]["msg_max"]

        #if self.confdict["log"]["console_level"].lower() == "level":
        for num,eachlevel in enumerate(self.LogLevelList):
            if self.confdict["log"]["console_level"].lower() == eachlevel:
                self.console_level = num
        #self.console_level = self.confdict["log"]["console_level"]
        for num,eachlevel in enumerate(self.LogLevelList):
            if self.confdict["log"]["log_level"].lower() == eachlevel:
                self.log_level = num

        # if gen.LoadDefaultConf is True:
        #     self.SetConfigDataOnUI()
        #     print "self.round_robin_scheduling",self.round_robin_scheduling
        #     gen.LoadDefaultConf = False

    def GenerateConfDict(self):

        # startup = self.startup
        # print "startup:",startup
        # tray_minimize = self.tray_minimize
        # print "tray_minimize:",tray_minimize
        # autoupdate = self.autoupdate
        # print "autoupdate", autoupdate

        # for name,item in map(None,["startup","tray_minimize","autoupdate"],[startup,tray_minimize,autoupdate]):
        #     if item is True:
        #         self.confdict["base"][name] = "true"
        #     else:
        #         self.confdict["base"][name] = "False"

        self.confdict["base"]["startup"] = self.startup_c.GetValue()
        self.confdict["base"]["tray_minimize"] = self.minicon_c.GetValue()
        self.confdict["base"]["autoupdate"] = self.checkupdate_c.GetValue()

        self.confdict["monitor"]["round_robin_scheduling"] = int(self.looptime_t.GetValue())

        data_file = self.datafile_t.GetValue()
        # if os.path.dirname(data_file) == os.getcwd():
        #     self.confdict["monitor"]["data_file"] = os.path.basename(data_file)
        # else:
        #     self.confdict["monitor"]["data_file"] = data_file
        if str(data_file).startswith(gen.CUR_PATH):
            self.confdict["monitor"]["data_file"] = str(data_file).split(gen.CUR_PATH+os.path.sep)[1]
        else:
            self.confdict["monitor"]["data_file"] = data_file

        # shutdown_monitor_cpu = self.cpu_c.GetValue()
        # if shutdown_monitor_cpu is True:
        #     self.confdict["monitor"]["shutdown_monitor_cpu"] = False
        # else:
        #    self.confdict["monitor"]["shutdown_monitor_cpu"] = True
        self.confdict["monitor"]["enable_monitor_cpu"] = self.cpu_c.GetValue()

        # shutdown_monitor_memory = self.memory_c.GetValue()
        # if shutdown_monitor_memory is True:
        #     self.confdict["monitor"]["shutdown_monitor_memory"] = False
        # else:
        #     self.confdict["monitor"]["shutdown_monitor_memory"] = True
        self.confdict["monitor"]["enable_monitor_memory"] = self.memory_c.GetValue()

        self.confdict["monitor"]["cpu_scheduling"] = int(self.loopTimeCpu_t.GetValue())
        self.confdict["monitor"]["memory_scheduling"] = int(self.loopTimeMemory_t.GetValue())

        # enable_console_show = self.closeconsole_c.GetValue()
        # if enable_console_show is True:
        #     self.confdict["log"]["enable_console_show"] = "true"
        # else:
        #     self.confdict["log"]["enable_console_show"] = "False"

        self.confdict["log"]["enable_console_show"] = self.enableconsole_c.GetValue()

        # enable_log = self.closelog_c.GetValue()
        # if enable_log is True:
        #     self.confdict["log"]["enable_log"] = "true"
        # else:
        #     self.confdict["log"]["enable_log"] = "False"
        self.confdict["log"]["enable_log"] =  self.enablelog_c.GetValue()

        log_file = self.logfile_t.GetValue()

        if str(log_file).startswith(gen.CUR_PATH):
            self.confdict["log"]["log_file"] = str(log_file).split(gen.CUR_PATH+os.path.sep)[1]
        else:
            self.confdict["log"]["log_file"] = log_file

        #self.confdict["log"]["log_file"] = self.logfile_t.GetValue()

        self.confdict["log"]["log_leave"] = int(self.logkeep_t.GetValue())
        self.confdict["log"]["log_size"] = int(self.logsize_t.GetValue())

        self.confdict["log"]["msg_max"] = int(self.clear_clog_t.GetValue())

        console_level = self.consolelevel_r.GetSelection()
        self.confdict["log"]["console_level"] = self.LogLevelList[console_level]

        log_level = self.loglevel_r.GetSelection()
        self.confdict["log"]["log_level"] = self.LogLevelList[log_level]
        return self.confdict

class settingDlg(wx.Dialog):
    def __init__(self,title,configdict):
        wx.Dialog.__init__(self, None, -1,title=title,size=(600,410),style=wx.DEFAULT_DIALOG_STYLE)#|wx.RESIZE_BORDER)

        self.panel = wx.Panel(self)
        #self.panel.SetBackgroundColour("white")
        self.SetUI = SettingPanel(self.panel,configdict)
        self.OKBtn = wx.Button(self.panel, label=u"确定",size=(80, 22),id=wx.ID_OK)
        self.CancelBtn = wx.Button(self.panel, label=u"取消",size=(80, 22),id=wx.ID_CANCEL)
        vsizer = wx.BoxSizer(wx.VERTICAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.SetUI,1,wx.EXPAND)

        vsizer.Add(hsizer,1,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add(self.OKBtn,0,wx.RIGHT|wx.ALIGN_RIGHT|wx.BOTTOM,border=10)
        hsizer2.Add(self.CancelBtn,0,wx.RIGHT|wx.ALIGN_RIGHT|wx.BOTTOM,border=10)

        vsizer.Add(hsizer2,0,wx.ALIGN_RIGHT|wx.RIGHT|wx.TOP, border=10)

        #hsizer = wx.BoxSizer(wx.HORIZONTAL)
        # sizer.Add(self.OKBtn, flag=wx.LEFT|wx.BOTTOM, border=5)
        # sizer.Add(self.CancelBtn, flag=wx.LEFT|wx.BOTTOM, border=5)

        #sizer.Add(hsizer,1,wx.EXPAND)
        self.panel.SetSizerAndFit(vsizer)


if __name__ == "__main__":
    import os
    from SettingData import HandleSetting
    app = wx.App()
    if  os.path.exists(gen.CONF_FILE) is  True:
        try:
            f = HandleSetting(gen.CONF_FILE)
            configdict = f.ReadConfFile()
        except:
            print "default dict"
            configdict = gen.DEFAULT_CONFIG_DICT
    else:
        print "default dict"
        configdict = gen.DEFAULT_CONFIG_DICT

    dlg = settingDlg(u"设置",configdict)
    print os.path.realpath(__file__)
    print os.path.relpath(__file__)
    dlg.Center()
    if dlg.ShowModal() == wx.ID_OK:
        newConfDict = dlg.SetUI.GenerateConfDict()
        #print newConfDict
        f = HandleSetting(gen.CONF_FILE,newConfDict)
        f.WriteConfFile()
        gen.CONF_DICT = newConfDict
        print type(gen.CONF_DICT["monitor"]["round_robin_scheduling"])
        print gen.LOOP_TIME
        print  type(gen.LOOP_TIME)
    dlg.Destroy()
    app.MainLoop()