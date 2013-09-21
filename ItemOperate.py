#coding:utf-8
import wx
import os
from dataList import DataHandle
from useValidator import InputValidator
import idDefine as gen
import LogOutput as LoadLog

class AddProgramDialog(wx.Dialog):
    def __init__(self,title,about=""):
        wx.Dialog.__init__(self, None, -1,title=title,style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        #self.OnExeSelectFile = eventHandle.OnExeSelectFile
        #self.OnLogSelectFile = eventHandle.OnLogSelectFile
        self.about_txt = about
        about_s   = wx.StaticText(self, -1, self.about_txt)
        name_s  = wx.StaticText(self, -1, u"程序名称:")
        fpath_s = wx.StaticText(self, -1, u"程序路径:")
        logpath_s = wx.StaticText(self, -1, u"参数或文件:")
        runAs_s = wx.StaticText(self,-1,u'启动方式:')
        proNum_s = wx.StaticText(self,-1,u'监控进程数:')
        note_s = wx.StaticText(self, -1, u"备注:")
        line = wx.StaticLine(self)

        ##单选框
        self.RadioList = [u"隐藏进程窗口",u"显示进程窗口"]
        self.runAsRadio = wx.RadioBox(self,-1, "", (-1,-1),
            (210,44),self.RadioList, 0, wx.RA_SPECIFY_COLS|wx.NO_BORDER)   ##单选框
        self.runAsRadio.SetSelection(1)

        #文本框，使用验证器
        self.name_t  = wx.TextCtrl(self,size=(210,22),       )
        self.fpath_t = wx.TextCtrl(self,size=(210,22), validator=InputValidator("fpath_t"))
        self.logpath_t = wx.TextCtrl(self,size=(210,22))
        #self.logpath_t = wx.TextCtrl(self,size=(210,22), validator=InputValidator("logpath_t"))
        self.note_t = note_t = wx.TextCtrl(self,size=(210,40))

        self.sampleList = [u'等于', u'小于', u'大于', u'小于或等于', u'大于或等于',u'不等于']
        self.operatorBox = wx.ComboBox(self, gen.ID_OPERATOR, "", (-1,-1), wx.DefaultSize, self.sampleList, wx.CB_READONLY)
        self.operatorBox.SetValue(self.sampleList[0])
        self.proNum_t = wx.SpinCtrl(self, -1,"",(10,80),(80,-1))
        self.proNum_t.SetRange(1,15)
        self.proNum_t.SetValue(1)

        self.monitor_t = wx.CheckBox(self, -1,u"开启监控",(35,80))

        self.fpath_b  = wx.Button(self, -1,size=(75,25), label=u"选择")
        self.logpath_b  = wx.Button(self, -1,size=(75,25),label= u"选择")

        okay   = wx.Button(self,id=wx.ID_OK, size=(75,25),label=u"确定")
        okay.SetDefault()
        cancel = wx.Button(self,id= wx.ID_CANCEL,size=(75,25),label=u"取消")

        gsizer = wx.GridBagSizer(8,4)
        ##程序名称
        gsizer.Add(about_s, pos=(0,0),span=(1,4),flag=wx.TOP|wx.LEFT, border=10)
        gsizer.Add(line, pos=(1,0), span=(1,4), flag=wx.EXPAND|wx.ALL, border=5)
        gsizer.Add(name_s, pos=(2,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT, border=10)
        gsizer.Add(self.name_t, pos=(2,1),span=(1,2),flag=wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border=5)
        ##程序文件
        gsizer.Add(fpath_s, pos=(3,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT, border=10)
        gsizer.Add(self.fpath_t, pos=(3,1),span=(1,2),flag=wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border=5)
        gsizer.Add(self.fpath_b, pos=(3,3),span=(1,1),flag=wx.ALIGN_LEFT|wx.RIGHT, border=10)
        ##日志
        gsizer.Add(logpath_s, pos=(4,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT, border=10)
        gsizer.Add(self.logpath_t, pos=(4,1),span=(1,2),flag=wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border=5)
        gsizer.Add(self.logpath_b, pos=(4,3),span=(1,1),flag=wx.ALIGN_LEFT|wx.RIGHT, border=10)
        ##单选框
        gsizer.Add(runAs_s, pos=(5,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT, border=10)
        gsizer.Add(self.runAsRadio, pos=(5,1),span=(2,2),flag=wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border=5)

        ##备注
        gsizer.Add(note_s, pos=(8,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT, border=10)
        gsizer.Add(note_t, pos=(8,1),span=(1,2),flag=wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border=5)
        ##监控
        gsizer.Add(proNum_s, pos=(7,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.LEFT, border=10)
        gsizer.Add(self.operatorBox, pos=(7,1),span=(1,1),flag=wx.ALIGN_LEFT|wx.LEFT|wx.EXPAND, border=5)
        gsizer.Add(self.proNum_t, pos=(7,2),span=(1,1),flag=wx.ALIGN_LEFT|wx.RIGHT, border=10)
        #gsizer.Add(self.monitor_t, pos=(7,2),span=(1,1),flag=wx.LEFT, border=30)
        gsizer.Add(self.monitor_t, pos=(7,3),span=(1,1),flag=wx.ALIGN_LEFT|wx.LEFT, border=0)
        ##按钮
        gsizer.Add(okay, pos=(9,2),span=(1,1),flag=wx.TOP|wx.BOTTOM|wx.ALIGN_RIGHT, border=10)
        gsizer.Add(cancel, pos=(9,3),span=(1,1),flag=wx.TOP|wx.BOTTOM|wx.RIGHT, border=10)

        gsizer.AddGrowableCol(1)
        gsizer.AddGrowableCol(2)
        gsizer.AddGrowableRow(8,1)
        self.SetSizer(gsizer)
        gsizer.Fit(self)
        gsizer.SetSizeHints(self)

        ##绑定可执行选择文件
        self.Bind(wx.EVT_BUTTON,self.OnExeSelectFile,self.fpath_b)
        ##绑定日志执行文件
        self.Bind(wx.EVT_BUTTON,self.OnLogSelectFile,self.logpath_b)

        self.Bind(wx.EVT_COMBOBOX,self.OnChoiceOperator,self.operatorBox,id=gen.ID_OPERATOR)


    def OnChoiceOperator(self,event):
        print u"选择的操作符：",self.operatorBox.GetValue()
        #self.operatorBox = self.operatorBox.GetValue()

    ##选择可执行文件对话框事件函数
    def OnExeSelectFile(self,event):
        wildcard = "Executable file (*.exe)|*.exe"
                    #"All files (*.*)|*.*"
        dialog = wx.FileDialog(self, u"选择文件", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            fpath =  dialog.GetPath()
            self.fpath_t.SetValue(fpath)
        dialog.Destroy()
    ##选择日志文件对话框事件函数
    def OnLogSelectFile(self,event):
        wildcard = "Log file (*.log)|*.log|" \
                    "Compiled file (*.txt)|*.txt|" \
                    "All files (*.*)|*.*"
        dialog = wx.FileDialog(self, u"选择文件", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            logpath =  dialog.GetPath()
            self.logpath_t.SetValue(logpath)
        dialog.Destroy()

    ##获取对话框输入的数据
    def  GetDialogData(self):
        self.name = self.name_t.GetValue()
        self.programe = self.fpath_t.GetValue()
        self.logfile = self.logpath_t.GetValue()
        self.processNum = self.proNum_t.GetValue()
        self.runAs = self.runAsRadio.GetSelection()
        self.note = self.note_t.GetValue()
        self.monitor = self.monitor_t.GetValue()
        self.operator = self.operatorBox.GetValue()
        print u"得到的操作符：",self.operatorBox.GetValue()
        LoadLog.LogMsg(gen.logger.info,u"返回对话框输入的数据")
        return self.name,self.programe,self.logfile,self.monitor,self.operator,self.processNum,self.runAs,self.note


class EditProgramDialog(AddProgramDialog):
    def __init__(self,title,about=""):
        AddProgramDialog.__init__(self,title=title,about=about)


    def SetDialogData(self,filename,item):
        ReadFromFile = DataHandle(filename)
        self.pdata = ReadFromFile.ReadData()
        print self.pdata[str(item)]
        self.name = self.pdata[str(item)]["name"]

        # if os.path.abspath(self.pdata[str(item)]["programe"]) is not True:
        #     self.programe = os.path.join(os.path.split(__file__)[0],self.pdata[str(item)]["name"])
        # else:
            #self.programe = self.pdata[str(item)]["name"]

        self.programe = os.path.abspath(self.pdata[str(item)]["programe"])

        self.logfile = self.pdata[str(item)]["logfile"]
        if  os.path.isfile(self.logfile):
            self.logfile = os.path.abspath(self.logfile)

        self.note = self.pdata[str(item)]["note"]
        self.monitor = self.pdata[str(item)]["monitor"]
        self.status = self.pdata[str(item)]["status"]
        self.operator = self.pdata[str(item)]["operator"]
        self.processNum = self.pdata[str(item)]["processNum"]
        self.runAs = self.pdata[str(item)]["runAs"]
        LoadLog.LogMsg(gen.logger.debug,u"获取对应项目的数据内容")
        #print "&&&&&&&&:",self.runAs

        LoadLog.LogMsg(gen.logger.debug,u"将取得项目的数据内容设定到编辑对话框")
        self.name_t.SetValue(self.name)
        self.fpath_t.SetValue(self.programe)
        self.logpath_t.SetValue(self.logfile)
        self.operatorBox.SetValue(self.operator)
        self.proNum_t.SetValue(self.processNum)
        #self.runAsRadio.SetSelection(0)
        self.runAsRadio.SetSelection(int(self.runAs))

        ProName = str(os.path.basename(self.programe))
        p = os.popen('tasklist /FI "IMAGENAME eq %s"' % ProName)
        GetProNum = p.read().count(ProName)
        #print "######### process Number: ###############",ProName,GetProNum,type(GetProNum)
        if GetProNum != 0 :
            self.runAsRadio.EnableItem(0,enable=False)
            self.runAsRadio.EnableItem(1,enable=False)
        self.note_t.SetValue(self.note)
        #print u"监控状态===>",self.monitor
        if self.monitor is True:
            self.monitor_t.SetValue(self.monitor)

if __name__ == "__main__":
    app = wx.App()
    #dlg = AddProgramDialog(u"添加程序")
    dlg = EditProgramDialog(u"编辑项目")
    dlg.SetDialogData("json.txt",1)
    dlg.Center()
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()