#coding:utf-8
import wx
import idDefine as gen
from useValidator import InputValidator
from ObjectListView import ObjectListView, ColumnDefn
from dataList import DataHandle
import LogOutput as LoadLog

class exportDialog(wx.Dialog):
    def __init__(self,title,filename,name="exportDialog"):
        LoadLog.LogMsg(gen.logger.debug,u"打开数据导出对话框")
        wx.Dialog.__init__(self, None, -1,title=title,style=wx.DEFAULT_DIALOG_STYLE)
        self.filename = filename
        self.panel = panel = wx.Panel(self,-1)
        self.plist = ObjectListView(panel,id=-1,size=(-1,-1),
                                           style=wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES|wx.BORDER_SUNKEN)

        self.setResults(self.filename)

        font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        text_information = wx.StaticText(panel,label=u"导出数据")
        text_information.SetFont(font)
        line = wx.StaticLine(panel)
        #self.SetBackgroundColour("while")

        selectbtn = wx.Button(panel,label=u"全选",size=(80,22),id=wx.ID_SELECTALL)
        unselectbtn = wx.Button(panel,label=u"取消",size=(80,22),id=gen.ID_UNSELECTALL)
        add_t = wx.StaticText(panel,label=u"导出位置：")
        self.path_t = path_t = wx.TextCtrl(panel,validator=InputValidator("save_path_t"),style=wx.TE_READONLY)
        #self.path_t.SetBackgroundColour("light blue")
        pathbtn = wx.Button(panel,label=u"选择",size=(80,25),id=wx.ID_SAVEAS)
        button_save = wx.Button(panel,label=u"确定",size=(80,25),id=wx.ID_OK)
        button_cancel = wx.Button(panel,label=u"取消",size=(80,25),id=wx.ID_CANCEL)

        sizer = wx.GridBagSizer(7,5)
        sizer.Add(text_information,pos=(0,0),span=(1,3),flag=wx.TOP|wx.LEFT, border=10)
        sizer.Add(line, pos=(1,0), span=(1,5), flag=wx.EXPAND|wx.TOP, border=0)
        sizer.Add(self.plist, pos=(2,0), span=(1,5), flag=wx.EXPAND|wx.RIGHT|wx.LEFT, border=10)
        sizer.Add(selectbtn,pos=(3,0),span=(1,1),flag=wx.RIGHT|wx.LEFT, border=10)
        sizer.Add(unselectbtn,pos=(3,1),span=(1,1),flag=wx.RIGHT|wx.LEFT, border=10)
        sizer.Add(add_t,pos=(4,0),span=(1,1),flag=wx.LEFT, border=10)
        sizer.Add(path_t,pos=(5,0),span=(1,4),flag=wx.EXPAND|wx.LEFT, border=10)
        sizer.Add(pathbtn,pos=(5,4),span=(1,1),flag=wx.RIGHT, border=10)
        sizer.Add(button_save,pos=(7,3),span=(1,1),flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_RIGHT, border=10)
        sizer.Add(button_cancel,pos=(7,4),span=(1,1),flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_RIGHT, border=10)
        #sizer.AddGrowableCol(0)
        panel.SetSizerAndFit(sizer)
        sizer.SetSizeHints(self)

        #self.OnSelectAll = self.evt.OnSelectAll

        self.Bind(wx.EVT_BUTTON,self.OnSelectAll,id=wx.ID_SELECTALL)
        self.Bind(wx.EVT_BUTTON,self.OnSelectAll,id=gen.ID_UNSELECTALL)
        self.Bind(wx.EVT_BUTTON,self.OnSelectFile,id=wx.ID_SAVEAS)

    def setResults(self,filename):
        self.plist.SetColumns([
            ColumnDefn(u"序号", "center", 40, "id"),
            ColumnDefn(u"名称", "left", 80, "name"),
            ColumnDefn(u"程序", "left", 120, "programe"),
            ColumnDefn(u"备注", "left", 100, "note"),
            ])
        self.plist.CreateCheckStateColumn()
        self.list_data = DataHandle(filename).handleList()
        self.plist.SetObjects(self.list_data)

    def OnSelectAll(self, event):
        objects = self.plist.GetObjects()
        for obj in objects:
            if event.GetId() == wx.ID_SELECTALL:
                self.plist.SetCheckState(obj, True)
            else:
                self.plist.SetCheckState(obj, False)
        self.plist.RefreshObjects(objects)

    def OnSelectFile(self,event):
        wildcard = "Json File (*.json)|*.json|" \
                    "All files (*.*)|*.*"
        dialog = wx.FileDialog(self, u"选择文件","", "", wildcard, wx.SAVE|wx.OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            self.filepath =  dialog.GetPath()
            self.path_t.SetValue(self.filepath)
        dialog.Destroy()

    def handleExportDlg(self):
        allobj = self.plist.GetObjects()
        tbool = []
        LoadLog.LogMsg(gen.logger.debug,u"检测选项")
        for obj in allobj:
            if self.plist.IsChecked(obj) == True:
                tbool.append(self.plist.IsChecked(obj))
        if tbool.count(True) == 0:
            LoadLog.LogMsg(gen.logger.warning,u"未选取任何要导出的项目")
            wx.MessageBox(u"未选取内容，没有数据导出", u'警告', wx.OK|wx.ICON_WARNING,parent=self.panel)
            return
        else:
            newDataDict = {}
            #print u"=====读取的文件：",self.filename
            readFileData = DataHandle(self.filename)

            pdata = readFileData.ReadData()
            #print u"====导出对话框从文件读取的字典：",pdata
            for obj in allobj:
                if self.plist.IsChecked(obj) == True:
                    kid = obj.kid
                    #print u"###选中的kid",kid
                    #print u"###字典，kid 对应的项",pdata[kid]
                    newDataDict[kid] = pdata[kid]
            try:
                print newDataDict
                exportObj = DataHandle(self.filepath)
                exportObj.WriteData(newDataDict)
                wx.MessageBox(u"数据文件成功导出！", u'信息', wx.OK|wx.ICON_INFORMATION)
                LoadLog.LogMsg(gen.logger.info,u"成功导出数据到文件")
            except:
                wx.MessageBox(u"保存文件出错，请检查文件权限", u'错误', wx.OK|wx.ICON_ERROR)
                LoadLog.LogMsg(gen.logger.warning,u"导出文件出错")
                return
    