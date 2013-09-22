# -*- coding: utf-8 -*-

import wx
import os
#import wx.aui
#import time

from ObjectListView import ObjectListView, ColumnDefn
from dataList import DataHandle
from eventHandle import EventHandle,EventSettingMenuAndLog
from monitorRun import MonitorPro
from  LogOutput import LogConsoleHandler
import LogOutput
import  LogOutput as LoadLog
import logging
import idDefine as gen
from  sysInformation import SysInfo
#from wx.lib.wordwrap import wordwrap
from SettingData import HandleSetting
from about import MyAboutBox

class TaskBarIcon(wx.TaskBarIcon):

    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon(name='icons/logo.ico', type=wx.BITMAP_TYPE_ICO), u'PMManager v1.0')
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)
        self.Bind(wx.EVT_MENU, self.OnShow, id=gen.ID_SHOW_WIN)
        self.Bind(wx.EVT_MENU, self.frame.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.font_bold = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self.font_bold.SetWeight(wx.BOLD)

    def OnTaskBarLeftDClick(self, event):
        if self.frame.IsIconized():
           self.frame.Iconize(False)
        if not self.frame.IsShown():
           self.frame.Show(True)
        self.frame.Raise()

    def OnShow(self, event):
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()

    def OnExit(self, event):
        self.frame.OnClose(event)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(gen.ID_SHOW_WIN, u'显示主窗口')
        menu.AppendSeparator()
        menu.Append(wx.ID_ABOUT, u'关于')
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT, u'退出')
        return menu

class TextSearchCtrl(wx.SearchCtrl):
    maxSearches = 5
    def __init__(self, parent, id=-1, value="",
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,doSearch=None):
        style |= wx.TE_PROCESS_ENTER
        wx.SearchCtrl.__init__(self, parent, id, value, pos, size, style)
        self.ShowCancelButton(True)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnTextEntered)
        self.Bind(wx.EVT_MENU_RANGE, self.OnMenuItem, id=1, id2=self.maxSearches)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel)
        self.doSearch = doSearch
        self.searches = []

    def OnTextEntered(self, evt):
        text = self.GetValue()
        if self.doSearch(text):
            self.searches.append(text)
            if len(self.searches) > self.maxSearches:
                del self.searches[0]
            #self.SetMenu(self.MakeMenu())
        self.SetValue("")

    def OnMenuItem(self, evt):
        text = self.searches[evt.GetId()-1]
        self.doSearch(text)

    def OnCancel(self,evt):
        self.SetValue("")

############# 主框架 ################################
class  MainFrame(wx.Frame):

    def __init__(self,title):
        wx.Frame.__init__(self,None,-1,title=title,size=(920,700))
        self.SetIcon(wx.Icon('icons/logo.ico', wx.BITMAP_TYPE_ICO))
        ##创建一个分割框架
        self.sp = wx.SplitterWindow(self)# 创建一个分割窗
        ##上框架为列表部分
        self.p1 = ProvPanel(self.sp,-1,style=wx.BORDER_SUNKEN|wx.TRANSPARENT_WINDOW)
        ##下框架为控制台与操作部分
        self.p2 = wx.Panel(self.sp,-1,style=wx.BORDER_SUNKEN)
        ## 设置上下框架上拉与下架的保留距离
        self.sp.SetMinimumPaneSize(50)
        ## 上框架默认距离
        self.sp.SplitHorizontally(self.p1,self.p2,180)

        ##使用 GridBagSizerr 布局
        p2Sizer = wx.GridBagSizer(hgap=5,vgap=5)
        self.logger = logging.getLogger("wxApp")

        self.LogTextUI()
        self.LoadData()

        self.LogButtonUI()
        p2Sizer.Add(self.nb, pos=(0,0),span=(5,4),flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.EXPAND, border=5)
        p2Sizer.Add(self.p2LogControl, pos=(0,4), span=(5,1),
                    flag=wx.RIGHT|wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_RIGHT|wx.EXPAND, border=5)

        p2Sizer.AddGrowableCol(1)
        p2Sizer.AddGrowableRow(1)
        self.p2.SetSizer(p2Sizer)
        self.p2.Fit()

        self.MenuUI()
        self.ToolBarUI()
        self.StatusBarUI()

        self.Centre()
        self.CallMonitor()
        self.CallSysInfoCPU()
        self.CallSysInfoMemory()
        self.taskBarIcon = TaskBarIcon(self)

        self.Bind(wx.EVT_CLOSE, self.OnHide)
        #self.Bind(wx.EVT_ICONIZE, self.OnHide)


    def OnHide(self,event):
        self.Hide()

    def OnClose(self, event):
        self.taskBarIcon.Destroy()
        self.Destroy()
        self.Close()

    def OnAbout(self,event):
        pass

    def LoadData(self):
        self.rf = rf = DataHandle(gen._filedata)
        self.pdata = rf.ReadData()

    def CallMonitor(self):
        LoadLog.LogMsg(gen.logger.info,u"加载监控")
        callMonFun = MonitorPro(gen.LOOP_TIME,self.pdata,self.rf,gen._filedata,self.p1.ProgrameList)
        wx.CallAfter(callMonFun.LoopDoMonitor)

    def CallSysInfoCPU(self):
        callSysInfoCPU = SysInfo()
        wx.CallAfter(callSysInfoCPU.getCPUstate)

    def CallSysInfoMemory(self):
        callSysInfoMemory = SysInfo()
        wx.CallAfter(callSysInfoMemory.getMemorystate)
#################菜单 UI #####################################
    def MenuUI(self):
        LoadLog.LogMsg(gen.logger.info,u"加载菜单")
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        viewMenu = wx.Menu()
        controlMenu = wx.Menu()
        aboutMenu = wx.Menu()
        fileMenu.Append(wx.ID_ADD, u'添加项目', u'添加项目')
        fileMenu.Append(wx.ID_DELETE, u'删除项目', u'删除项目')
        fileMenu.Append(wx.ID_EDIT, u'编辑项目', u'编辑项目')
        fileMenu.AppendSeparator()
        fileMenu.Append(gen.ID_IMPORT, u'导入数据', u'导入数据')
        fileMenu.Append(gen.ID_EXPORT, u'导出数据', u'导出数据')
        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_SETUP, u'设置', u'设置')
        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_EXIT, u'退出',u'退出')
        viewMenu.Append(gen.ID_VIEW, u'查看日志文件', u'查看日志文件')
        controlMenu.Append(gen.ID_START, u'启动进程', u'启动进程')
        controlMenu.Append(gen.ID_STOP, u'停止进程', u'停止进程')
        controlMenu.Append(gen.ID_RESTART, u'重启进程', u'重启进程')
        controlMenu.AppendSeparator()
        #controlMenu.Append(gen.ID_MONITOR, u'监控服务', '')
        #controlMenu.Append(gen.ID_MONITOR, u'取消监控', '')
        aboutMenu.Append(wx.ID_HELP,u'查看帮助',u"查看帮助")
        aboutMenu.Append(wx.ID_ABOUT,u'关于',u"关于")

        menubar.Append(fileMenu, u'文件')
        menubar.Append(viewMenu, u'查看')
        menubar.Append(controlMenu, u'控制')
        menubar.Append(aboutMenu,u'帮助')
        self.SetMenuBar(menubar)

        ###### 菜单绑定事件
        self.Bind(wx.EVT_MENU,self.OnClose, id=wx.ID_EXIT)
        ##获取一个列表控件的实例
        self.ProgrameList = ProgrameList = self.p1.ProgrameList

        ##将数据文件和实例传递给类EventHandle 得到一个关于事件的实例
        self.evt = EventHandle(gen._filedata,ProgrameList)

        ##实例调用EventHandle 类的一个对话框事件方法
        ##事件绑定于添加程序对话框
        self.Bind(wx.EVT_MENU,self.evt.OnAdd_Edit_Dialog,id=wx.ID_ADD)
        self.Bind(wx.EVT_MENU,self.evt.OnAdd_Edit_Dialog,id=wx.ID_EDIT)
        self.Bind(wx.EVT_MENU,self.evt.OnDelDialog,id=wx.ID_DELETE)

        self.Bind(wx.EVT_MENU,self.evt.OnExportDlg,id=gen.ID_EXPORT)
        self.Bind(wx.EVT_MENU,self.evt.OnImportDlog,id=gen.ID_IMPORT)

        self.Bind(wx.EVT_MENU,self.evt.OnOperationPro,id=gen.ID_START)
        self.Bind(wx.EVT_MENU,self.evt.OnOperationPro,id=gen.ID_STOP)
        self.Bind(wx.EVT_MENU,self.evt.OnOperationPro,id=gen.ID_RESTART)



        self.menu_evt = EventHandle()

        self.Bind(wx.EVT_MENU,self.menu_evt.OnOpenLogFile,id=gen.ID_VIEW)
        self.menu_setting_evt  = EventSettingMenuAndLog(self.MonitorButton,self.StopMButton,
                                                       self.RefreshButton,self.LogName.ConsoleText,self.IntervalBox)
        self.Bind(wx.EVT_MENU,self.menu_setting_evt.OnSettingUI,id=wx.ID_SETUP)

        self.Bind(wx.EVT_MENU,self.OnAbout,id=wx.ID_ABOUT)

        self.Bind(wx.EVT_MENU,self.menu_evt.OnHelp,id=wx.ID_HELP)

    def OnAbout(self,event):
        about = MyAboutBox(self)
        about.ShowModal()
        about.Destroy()
        # info = wx.AboutDialogInfo()
        # about_icon = wx.Icon('icons\logo.png', wx.BITMAP_TYPE_PNG)
        # info.SetIcon(about_icon)
        # info.Name = u"PMManager 进程监控管理器"
        # info.Version = "v1.0"
        # info.Description = wordwrap(u"欢迎使用! PMManager 是一个免费的进程监控的管理软件，用于监控正在运行的进程，"
        #                        u"当发现进程被关闭时可以自动开启，同时也可以启动，结束，重启进程。"
        #                        u"他使用 python 语言编写。 ",420, wx.ClientDC(self))
        #
        # info.WebSite = ("https://github.com/avyou", u"主页")
        # info.Developers = [u"赵子发(avyou55@gamil.com)"]
        # info.License = wordwrap(u"免费软件!", 420,
        #                     wx.ClientDC(self))
        # info.SetCopyright(u'(C) 2013 赵子发(avyou)')
        # wx.AboutBox(info)
############工具栏 ############################################
    def ToolBarUI(self):
        LoadLog.LogMsg(gen.logger.info,u"加载工具栏")
        toolbar = self.CreateToolBar(style = wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_TEXT)
        ## 定义一个工具栏的间隔距离
        tsize = (56,32)
        toolbar.SetToolBitmapSize(tsize)

        #####定义工具栏的位图
        add_tmp = wx.Bitmap("img/c1.png",wx.BITMAP_TYPE_ANY)
        del_tmp = wx.Bitmap("img/c2.png",wx.BITMAP_TYPE_ANY)
        edit_tmp = wx.Bitmap("img/c3.png",wx.BITMAP_TYPE_ANY)
        start_tmp = wx.Bitmap("img/c4.png",wx.BITMAP_TYPE_ANY)
        restart_tmp = wx.Bitmap("img/c5.png",wx.BITMAP_TYPE_ANY)
        stop_tmp = wx.Bitmap("img/prestart.png",wx.BITMAP_TYPE_ANY)

        ###添加工具栏标签
        toolbar.AddLabelTool(wx.ID_ADD,u"添加项目",add_tmp,shortHelp=u"添加项目",longHelp=u"")
        toolbar.AddLabelTool(wx.ID_DELETE,u"删除项目",del_tmp,shortHelp=u"删除项目",longHelp=u"")
        toolbar.AddLabelTool(wx.ID_EDIT,u"编辑项目",edit_tmp,shortHelp=u"编辑项目",longHelp=u"")
        toolbar.AddSeparator()
        toolbar.AddLabelTool(gen.ID_START,u"启动进程",start_tmp,shortHelp=u"启动进程",longHelp=u"")
        toolbar.AddLabelTool(gen.ID_STOP,u"结束进程",restart_tmp,shortHelp=u"结束进程",longHelp=u"")
        toolbar.AddLabelTool(gen.ID_RESTART,u"重启进程",stop_tmp,shortHelp=u"重启进程",longHelp=u"")
        ##分隔线
        toolbar.AddSeparator()
        toolbar.AddStretchableSpace()
        search = TextSearchCtrl(toolbar, size=(150,-1), doSearch=self.DoSearch)
        toolbar.AddControl(search)
        # toolbar.AddLabelTool(ID_MONITOR,"",wx.Bitmap("img/pstart.png",wx.BITMAP_TYPE_ANY),shortHelp=u"监控程序",longHelp=u"")
        # toolbar.AddLabelTool(ID_NOMONITOR,"",wx.Bitmap("img/Security.png",wx.BITMAP_TYPE_ANY),shortHelp=u"取消监控",longHelp=u"")
        # toolbar.AddLabelTool(ID_NOMONITOR,"",wx.Bitmap("img/psearch.png",wx.BITMAP_TYPE_ANY),shortHelp=u"取消监控",longHelp=u"")
        # #toolbar.AddLabelTool(wx.ID_EXIT,"",wx.Bitmap("img/exit.png",wx.BITMAP_TYPE_ANY),shortHelp=u"取消监控",longHelp=u"")
        #toolbar.SetBackgroundColour("white")
        toolbar.Realize()

    def DoSearch(self,  text):
        self.menu_setting_evt  = EventSettingMenuAndLog(self.MonitorButton,self.StopMButton,
                                                       self.RefreshButton,self.LogName.ConsoleText,self.IntervalBox)
        self.menu_setting_evt.FindString(text)
    def OnCombo(self):
        pass

    ###状态栏
    def StatusBarUI(self):
        self.statusbar = CustomStatusBar(self)
        self.SetStatusBar(self.statusbar)

    ##日志页面
    # def LogPageUI(self):
    #     self.nb = nb = wx.Notebook(self.p2)
    #     keys_list = [u"Console"]
    #     for kid in self.pdata.keys():
    #         keys_list.append(self.pdata[kid]["name"])
    #     for LogName in keys_list:
    #         title = u"  %s  " % LogName
    #         LogName = LogPage(nb)
    #         nb.AddPage(LogName, title)
    #     sizer = wx.BoxSizer()
    #     sizer.Add(nb, 1, wx.EXPAND)
    #     self.p2.SetSizer(sizer)

    def LogTextUI(self):
        LoadLog.LogMsg(gen.logger.info,u"加载消息控制台")
        self.nb = wx.Notebook(self.p2)
        #self.lognb = wx.aui.AuiNotebook(self.p2)
        self.LogName = LogPage(self.nb)
        self.nb.AddPage(self.LogName, u"消息控制台")
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.p2.SetSizer(sizer)

    # def LogPageUI(self):
    #     self.nb = nb = wx.Notebook(self.p2)
    #     LogName = LogPage(nb)
    #     nb.AddPage(LogName, "test")
    #     sizer = wx.BoxSizer()
    #     sizer.Add(nb, 1, wx.EXPAND)
    #     self.p2.SetSizer(sizer)

    ##日志控制面板
    def LogButtonUI(self):
        LoadLog.LogMsg(gen.logger.info,u"加载日志控制面板")
        self.p2LogControl = p2LogControl = wx.StaticText(self.p2,-1,"",size=(50,-1))
        boxsizer = wx.BoxSizer(wx.VERTICAL)
        boxLogControl = wx.StaticBox(p2LogControl,-1,label=u"控制台日志操作",size=(100,-1))
        #lbSizer.Add(boxLogControl,1,flag=wx.EXPAND|wx.TOP,border=15)
        sboxsizer = wx.StaticBoxSizer(boxLogControl, wx.VERTICAL)
        self.MonitorButton = MonitorButton = wx.Button(p2LogControl,id=gen.ID_MONITOR,label = u"开启查看")
        self.StopMButton = StopMButton = wx.Button(p2LogControl,id=gen.ID_STOP_MONITOR,label = u"停止查看")
        self.RefreshButton = RefreshButton = wx.Button(p2LogControl,id=gen.ID_REFRESH_MONITOR,label = u"清空日志")
        RefreshText = wx.StaticText(p2LogControl,-1,label = u"自动清空大小(字节)")

        self.IntervalBox = IntervalBox = wx.ComboBox(p2LogControl, gen.ID_REFERSH_INTERVA, "", (15,30), wx.DefaultSize, gen.SAMPLELIST, wx.CB_DROPDOWN)
        sboxsizer.Add(MonitorButton,0,wx.TOP|wx.EXPAND,10)
        sboxsizer.Add(StopMButton,0,wx.TOP|wx.EXPAND,10)
        sboxsizer.Add(RefreshButton,0,wx.TOP|wx.EXPAND,10)
        sboxsizer.Add(RefreshText,0,wx.TOP|wx.EXPAND,20)
        sboxsizer.Add(IntervalBox,0,wx.TOP|wx.EXPAND,5)
        boxsizer.Add(sboxsizer,1,wx.EXPAND|wx.TOP,15)
        p2LogControl.SetSizerAndFit(boxsizer)

        confObj = HandleSetting(gen.CONF_FILE)
        print confObj.ReadSingleConf("log","enable_console_show")
        if confObj.ReadSingleConf("log","enable_console_show") is True:
            MonitorButton.Disable()
        else:
            StopMButton.Disable()

        self.evt_log = EventSettingMenuAndLog(MonitorButton,StopMButton,RefreshButton,self.LogName.ConsoleText,IntervalBox)
        self.Bind(wx.EVT_BUTTON, self.evt_log.OnViewLog,MonitorButton)
        self.Bind(wx.EVT_BUTTON, self.evt_log.OnStopLog,StopMButton)
        self.Bind(wx.EVT_BUTTON, self.evt_log.OnClearLog,RefreshButton)
        self.Bind(wx.wx.EVT_COMBOBOX,self.evt_log.OnClearMax,self.IntervalBox)
        #self.Bind(wx.EVT_TEXT,self.evt_log.OnClearMax,self.IntervalBox)

class ProvPanel(wx.Panel):
    def __init__(self, parent,id,style):
        LoadLog.LogMsg(gen.logger.info,u"加载下边框架面板")
        wx.Panel.__init__(self,id=id, parent=parent,style=style)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour("while")
        self.ProgrameList = ObjectListView(self,id=wx.ID_VIEW_LIST,size=(-1,50),
                                           style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_VRULES|wx.LC_HRULES)

        #self.ProgrameList.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK
        self.setResults(gen._filedata)

        self.ListButtonUI()
        ##列表控件布局
        vSizer.Add(self.ProgrameList, 1, wx.EXPAND|wx.ALL, 5)
        ##按钮的布局
        vSizer.Add(self.sSizer, 0,wx.ALL, 2)
        self.SetSizerAndFit(vSizer)

        ##双击列表事件绑定
        self.evt = EventHandle(gen._filedata,self.ProgrameList)
        ##实例调用EventHandle 类的一个对话框事件方法
        self.OnAdd_Edit_Dialog = self.evt.OnAdd_Edit_Dialog
        self.ProgrameList.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.OnAdd_Edit_Dialog,id=wx.ID_VIEW_LIST)

    def setResults(self,filename):
        self.ProgrameList.SetColumns([
            ColumnDefn(u"序号", "left", 40, "id"),
            ColumnDefn(u"名称", "left", 100, "name"),
            ColumnDefn(u"程序", "left", 150, "programe"),
            ColumnDefn(u"参数", "left", 150, "logfile"),
            ColumnDefn(u"状态", "center", 60, "status"),
            ColumnDefn(u"监控", "left", 40, "monitor"),
            ColumnDefn(u"条件", "center", 50, "operator"),
            ColumnDefn(u"进程数", "left", 50, "processNum"),
            ColumnDefn(u"启动方式", "center", 60, "runAs"),
            ColumnDefn(u"备注", "left", 150, "note"),
            ])
        ##使用checkBox 复选框
        self.ProgrameList.CreateCheckStateColumn()
        self.SetDataInListctrl(filename)

    def SetDataInListctrl(self,filename):
        LoadLog.LogMsg(gen.logger.info,u"加载控件列表，初始化数据")
        ##获取数据列表
        self.list_data = DataHandle(filename).handleList()
        ##设置数据列表到列表控件
        self.ProgrameList.SetObjects(self.list_data)

    ##列表控件下面的按钮
    def ListButtonUI(self):
        self.sSizer = sSizer = wx.BoxSizer(wx.HORIZONTAL)
        SelectAllButton = wx.Button(self,id=wx.ID_SELECTALL,size=(50,22),label = u"全选")
        RSelectAllButton = wx.Button(self,id=gen.ID_UNSELECTALL,size=(50,22),label = u"取消")
        #ClearButton = wx.Button(self,id=gen.ID_SELECTCLEAR,size=(50,22),label = u"测试")
        #ImportButton = wx.Button(self,id=gen.ID_IMPORT,size=(50,22),label = u"导入")
        #ExportButton = wx.Button(self,id=gen.ID_EXPORT,size=(50,22),label = u"导出")
        sSizer.Add(SelectAllButton,0,wx.LEFT,2)
        sSizer.Add(RSelectAllButton,0,wx.LEFT,10)
        #sSizer.Add(ClearButton,0,wx.LEFT,10)
        #sSizer.Add(ImportButton,0,wx.LEFT,10)
        #sSizer.Add(ExportButton,0,wx.LEFT,10)

        self.evt = EventHandle(gen._filedata,self.ProgrameList)
        self.Bind(wx.EVT_BUTTON,self.evt.OnSelectAll,id=wx.ID_SELECTALL)
        self.Bind(wx.EVT_BUTTON,self.evt.OnSelectAll,id=gen.ID_UNSELECTALL)
        #self.Bind(wx.EVT_BUTTON,self.OndisplayValue,id=ID_SELECTCLEAR)

class CustomStatusBar(wx.StatusBar):
    def __init__(self,parent):
        wx.StatusBar.__init__(self, parent, -1)
        LoadLog.LogMsg(gen.logger.info,u"加载状态栏")
        self.SetFieldsCount(6)
        self.SetStatusWidths([-2,-1,-2,-1,-1,-1])
        self.sizeChanged=True
        #self.Bind(wx.EVT_SIZE,self.OnSize)
        #self.SetStatusText(u"状态栏测试",0)
        self.SetStatusText("aaa",1)
        # self.SetStatusText(gen.monProNum,1)
        #self.SetStatusText(gen.runProNum,2)
        self.timer=wx.PyTimer(self.Notify)
        self.timer.Start(1000)
        self.Notify()
    def Notify(self):
        #t=time.localtime(time.time())
        #st=time.strftime("%Y-%m-%d %H:%M:%S",t)

        allProNum = u"项目总数："
        monProNum = u"监控的项目数: "
        runProNum = u"运行的项目数: "
        #mem = wx.GetFreeMemory()
        #self.SetStatusText(mem,0)
        self.SetStatusText(gen.CPU,1)
        self.SetStatusText(gen.MEMORY,2)
        self.SetStatusText(allProNum + str(gen.allProNum),3)
        self.SetStatusText(monProNum + str(gen.monProNum),4)
        self.SetStatusText(runProNum + str(gen.runProNum),5)

class LogPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ConsoleText = ConsoleText = wx.TextCtrl(self,-1, "", size=(-1,-1),style=wx.TE_MULTILINE)#|wx.TE_RICH2)
        ConsoleText.SetBackgroundColour("light blue")
        boxsizer.Add(ConsoleText,1,flag=wx.EXPAND)

        self.SetSizerAndFit(boxsizer)

        ##文本框使用日志
        LoadLog.LogMsg(gen.logger.warning,u"初始化控制台")
        txtHandler = LogConsoleHandler(ConsoleText)
        gen.logger.addHandler(txtHandler)

    def ClearLog(self):
        self.ConsoleText.SetValue("")


class MySplashScreen(wx.SplashScreen):

    def __init__(self, parent=None):
        aBitmap = wx.Image(name = "Img/startup.jpg").ConvertToBitmap()
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
        splashDuration = gen.SPLASH_TIME
        wx.SplashScreen.__init__(self, aBitmap, splashStyle,splashDuration, parent)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        wx.Yield()

    def OnExit(self, evt):
        self.Hide()
        LogOutput.LogMain()
        frame = MainFrame(u"PMManager v1.0 |  欢迎使用")
        frame.Show(True)
        evt.Skip()

class MyApp(wx.App):
    def OnInit(self):
        ##获取实例名称
        self.name = "%s-%s" % (self.GetAppName(), wx.GetUserId())
        ##要检测的实例
        self.instance = wx.SingleInstanceChecker(self.name)
        ##查看实例是否已经运行，如果已经运行则初始化失败退出
        if self.instance.IsAnotherRunning():
            wx.MessageBox(u"PMManager 进程监控管理器，已经在运行了！",u"提示")
            return False
        ##检测有没有数据文件，如果没有创建一个空白数据文件
        CheckDataFileExists(gen._filedata)
        MySplash = MySplashScreen()
        MySplash.Show()
        return True

def CheckDataFileExists(filename):
    if os.path.exists(filename) is False:
        with open(filename,"w") as f:
            f.write("{}")

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()