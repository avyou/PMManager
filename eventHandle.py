#coding:utf-8
import wx
import time
#import codecs
import os,win32api,sys
#from wx.lib.wordwrap import wordwrap
import logging
from ItemOperate import AddProgramDialog,EditProgramDialog
from InExport import exportDialog
from dataList import DataHandle
import idDefine as gen
import subprocess
import LogOutput as LoadLog
from SettingUI import settingDlg
from SettingData import HandleSetting
from HelpDoc import HtmlDocDlg

class EventHandle(object):
    def __init__(self,filename=None,plist=None):
        self.filename = filename
        ##传入列表控件对象
        self.ProgrameList = plist
        self.datahandle = DataHandle(self.filename)

    def OnAdd_Edit_Dialog(self,event):
        #print "add_edit_dialog"
        if event.GetId() == wx.ID_ADD:
            self.dlg = AddProgramDialog(u"增加项目",u"请输入添加项目的相关内容:")
            LoadLog.LogMsg(gen.logger.info,u"打开增加对话框")
            self.kid = None
        elif event.GetId() == wx.ID_EDIT:
            self.kid = self.CheckEdit()
            if self.kid is None:
                return
            self.dlg = EditProgramDialog(u"编辑项目",u"请输入编辑项目的相关内容:")
            LoadLog.LogMsg(gen.logger.info,u"打开编辑对话框")
            self.dlg.SetDialogData(self.filename,self.kid)

        ########## 双击事件 #############
        elif event.GetId() == wx.ID_VIEW_LIST:
            rowObj = self.ProgrameList.GetSelectedObject()
            self.kid = rowObj.kid
            ##清空选择
            self.OnSelectAll()
            ##在双击的行上选择
            allobj = self.ProgrameList.GetObjects()
            self.ProgrameList.SetCheckState(rowObj, True)
            ##需要刷新对象
            self.ProgrameList.RefreshObjects(allobj)

            self.dlg = EditProgramDialog(u"编辑项目",u"请输入编辑程序的相关内容:")
            LoadLog.LogMsg(gen.logger.info,u"打开编辑对话框")
            #kid = "5"
            self.dlg.SetDialogData(self.filename,self.kid)
        else:
            return
        #addpdlg.ShowModal()
        ##增加程序数据
        if self.dlg.ShowModal() == wx.ID_OK:
            ##对话框获取返回的数据
            name,programe,logfile,monitor,operator,processNum,runAs,note = self.dlg.GetDialogData()
            kid = self.kid

            ##对话框返回的数据，调用增加数据的方法来处理
            #print "#####processNum:",processNum
            #print "#####runAs:",runAs
            LoadLog.LogMsg(gen.logger.debug,u"取得对话框的数据")
            self.datahandle.Add_Edit_Data(kid,name,programe,logfile,monitor,operator,processNum,runAs,note)
            ##调用handleList()方法，得到给列表控件显示的数据
            gen.IsRunStatusChanged = True
            list_data = self.datahandle.handleList()
            #print u"handle_list处理后显示给列表控件的值",list_data
            ##设置列表控件数据显示
            LoadLog.LogMsg(gen.logger.debug,u"刷新控件列表")
            self.ProgrameList.SetObjects(list_data)
            gen.IsItemChanged = True

        self.dlg.Destroy()

    def OnDelDialog(self,evnt):
        allobj = self.ProgrameList.GetObjects()
        tbool = []
        for obj in allobj:
            tbool.append(self.ProgrameList.IsChecked(obj))
        if tbool.count(True) == 0:
            LoadLog.LogMsg(gen.logger.info,u"未选择删除项")
            wx.MessageBox(u"至少选择一行进行删除！", u'信息', wx.OK | wx.ICON_INFORMATION,parent=self.ProgrameList)
            return
        else:
            pdata = self.datahandle.ReadData()
            #print u"==删除字典项前，从文件读取的字典数据:",pdata
            delList = []
            for obj in allobj:
                if self.ProgrameList.IsChecked(obj) == True:
                    kid = obj.kid
                    #print u"==删除选中的kid ====> ",kid
                    #print pdata[kid]
                    delList.append(kid)
            ##提示是否要删除
            delQuestionDlg =  wx.MessageDialog(self.ProgrameList,u"是否确认要删除所选内容？", u'确认提示',
                                               wx.YES_NO|wx.ICON_QUESTION)
            if delQuestionDlg.ShowModal() == wx.ID_YES:
                LoadLog.LogMsg(gen.logger.warning,u"删除数据项")
                for keyid in delList:
                    ##从列表中删除选中字典项
                    del pdata[keyid]
                self.datahandle.WriteData(pdata)
                list_data = self.datahandle.handleList()
                self.ProgrameList.SetObjects(list_data)
                gen.IsItemChanged = True
            else:
                LoadLog.LogMsg(gen.logger.debug,u"取消删除项")
                self.OnSelectAll()
                del delList
            #self.ProgrameList.RefreshObjects(allobj)
            return
            #datahandle = DataHandle(self.filename)
            #datahandle.WriteData()

    def OnExportDlg(self,event):
        #print "=== onExport dialog ==="
        self.dlg = exportDialog(u"导出数据",self.filename)
        if self.dlg.ShowModal() == wx.ID_OK:
            self.dlg.handleExportDlg()
        self.dlg.Destroy()

    def OnImportDlog(self,event):
        LoadLog.LogMsg(gen.logger.info,u"打开导入对话框")
        wildcard = "Json File (*.json)|*.json|" \
                   "All files (*.*)|*.*"

        importDlg = wx.FileDialog(None, u"选择导入的文件",os.getcwd(), "", wildcard, wx.OPEN)
        if importDlg.ShowModal() == wx.ID_OK:
            ipathfile = importDlg.GetPath()
            importObj = DataHandle(ipathfile)
            pdata = importObj.ReadData()
            #print u"===从导入文件读取到的字典： ",pdata
            if pdata != None:
                for eachKey in pdata.keys():
                    if eachKey.isdigit():
                        break
                subkeys = ["status","name","runAs","note","programe","processNum","kid","logfile","monitor"]
                for kid in pdata.keys():
                    if len(pdata[kid].keys()) != len(subkeys):
                        break
                    for eachsubKey in subkeys:
                        if eachsubKey not in pdata[kid]:
                            break
                #print u"===从导入文件读取到,并通过的字典：",pdata
                writeDlg = wx.MessageDialog(self.ProgrameList,u"导入的文件数据将覆盖现在程序的数据，是否继续?", u'确认提示',
                                               wx.YES_NO|wx.ICON_QUESTION)
                if writeDlg.ShowModal() == wx.ID_YES:
                    saveObj = DataHandle(self.filename)
                    saveObj.WriteData(pdata)
                    LoadLog.LogMsg(gen.logger.info,u"成功导入")
                    list_data = self.datahandle.handleList()
                    LoadLog.LogMsg(gen.logger.info,u"刷新控件列表")
                    self.ProgrameList.SetObjects(list_data)
                else:
                    LoadLog.LogMsg(gen.logger.info,u"取消导入")
                    return
            else:
                wx.MessageBox(u"无法导入，类型或错误的文件结构", u'错误', wx.OK | wx.ICON_ERROR)
                LoadLog.LogMsg(gen.logger.error,u"无法导入，类型或错误的文件结构")
        importDlg.Destroy()

    def CheckEdit(self):
        allobj = self.ProgrameList.GetObjects()
        tbool = []
        for obj in allobj:
            tbool.append(self.ProgrameList.IsChecked(obj))
        if tbool.count(True) == 0:
            LoadLog.LogMsg(gen.logger.info,u"未选取项目进行编辑")
            wx.MessageBox(u"请选择一行进行编辑", u'信息', wx.OK | wx.ICON_INFORMATION,parent=self.ProgrameList)
            self.kid = None
        elif tbool.count(True) > 1:
            LoadLog.LogMsg(gen.logger.info,u"不能选取多项同时进行编辑")
            wx.MessageBox(u"一次只能选择一行进行编辑", u'信息', wx.OK | wx.ICON_INFORMATION,parent=self.ProgrameList)
            ##清空选择
            self.OnSelectAll()
            self.kid = None
        else:
            rowObj = self.ProgrameList.GetObjects()
            for obj in rowObj:
                if self.ProgrameList.IsChecked(obj) == True:
                    self.kid = obj.kid
        return self.kid

    def OnSelectAll(self,event=None):
        objects = self.ProgrameList.GetObjects()
        for obj in objects:
            if event == None:
                self.ProgrameList.SetCheckState(obj, False)
            elif event.GetId() == wx.ID_SELECTALL:
                self.ProgrameList.SetCheckState(obj, True)
            else:
                self.ProgrameList.SetCheckState(obj,False)
        self.ProgrameList.RefreshObjects(objects)


    def OnOperationPro(self,event):
        processKidList = []
        objects = self.ProgrameList.GetObjects()
        for obj in objects:
            if self.ProgrameList.IsChecked(obj):
                kid = obj.kid
                processKidList.append(kid)

        if len(processKidList) == 0:
             wx.MessageBox(u"请选择一项进行操作", u'信息', wx.OK | wx.ICON_INFORMATION,parent=self.ProgrameList)
             LoadLog.LogMsg(gen.logger.info,u"未选取项目")
             return

        pdata = self.datahandle.ReadData()
        for kid in processKidList:
            pLastName = pdata[kid]["programe"]
            Pro_Argument = pdata[kid]["logfile"]

            #print u"获取到可执行的程序名称",pLastName
            ProName = str(os.path.basename(pLastName))
            p = os.popen('tasklist /FI "IMAGENAME eq %s"' % ProName)
            GetProNum = p.read().count(ProName)
            if GetProNum == "":
                GetProNum = 0
            LoadLog.LogMsg(gen.logger.debug,u"获取%s进程数为 %d" % (ProName,GetProNum))

            if event.GetId() == gen.ID_START:
                if GetProNum == pdata[kid]["processNum"] :
                    wx.MessageBox(u"该项目的进程已经在运行中", u'提示信息', wx.OK | wx.ICON_INFORMATION,parent=self.ProgrameList)
                    LoadLog.LogMsg(gen.logger.info,u"该项目的进程%s已经在运行中" % pLastName)
                else:
                    LoadLog.LogMsg(gen.logger.info,u"启动进程%s" % pLastName)
                    try:
                        a = win32api.ShellExecute(0, 'open', pLastName, Pro_Argument,'',1)
                        #self.UpdateRunStatus(kid,True)
                        gen.IsRunStatusChanged = True
                        pdata[kid]["status"] = True
                        list_data = self.datahandle.handleList(pdata)
                        self.ProgrameList.SetObjects(list_data)
                    except:
                         LoadLog.LogMsg(gen.logger.warning,u"启动进程: %s失败" % ProName)

            elif event.GetId() == gen.ID_STOP:
                #print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa::::::",pdata[kid]["monitor"]
                if GetProNum != 0 :
                    StopDlg =  wx.MessageDialog(self.ProgrameList,u"您确定要结束该进程吗？", u'确认提示',
                                               wx.YES_NO|wx.YES_NO)
                    if StopDlg.ShowModal() == wx.ID_YES:
                        try:
                            LoadLog.LogMsg(gen.logger.warning,u"结束进程: %s" % ProName)
                            subprocess.Popen("taskkill /F /im  %s" % os.path.basename(pLastName) , shell=True)
                            #self.UpdateRunStatus(kid,False)
                            gen.IsRunStatusChanged = True
                            pdata[kid]["status"] = False
                            list_data = self.datahandle.handleList(pdata)
                            self.ProgrameList.SetObjects(list_data)
                        except:
                             LoadLog.LogMsg(gen.logger.warning,u"结束进程: %s失败" % ProName)
                    StopDlg.Destroy()
                else:
                    LoadLog.LogMsg(gen.logger.info,u"当前项目未运行，没有进程可结束")
            else:
                RestartDlg =  wx.MessageDialog(self.ProgrameList,u"您确定要重启该进程吗？", u'确认提示',
                                                   wx.YES_NO|wx.ICON_QUESTION)
                if RestartDlg.ShowModal() == wx.ID_YES:
                    if GetProNum != 0 :
                        LoadLog.LogMsg(gen.logger.info,u"当前项目未运行，没有进程可结束")
                    try:
                        LoadLog.LogMsg(gen.logger.warning,u"重启进程: %s" % ProName)
                        subprocess.Popen("taskkill /F /im  %s" % os.path.basename(pLastName) , shell=True)
                        gen.IsRunStatusChanged = True
                        pdata[kid]["status"] = False
                        time.sleep(2)
                        self.a = win32api.ShellExecute(0, 'open', pLastName, Pro_Argument,'',1)
                        pdata[kid]["status"] = True
                        list_data = self.datahandle.handleList(pdata)
                        self.ProgrameList.SetObjects(list_data)

                    except:
                        LoadLog.LogMsg(gen.logger.warning,u"重启进程: %s失败" % ProName)
                RestartDlg.Destroy()
        processKidList = []

    # def UpdateRunStatus(self,kid,isRun):
    #     LoadLog.LogMsg(gen.logger.debug,u"更新运行状态")
    #     datahandle = DataHandle(self.filename)
    #     pdata = datahandle.ReadData()
    #     if pdata[kid]["monitor"] == True:
    #         pdata[kid]["status"] = isRun
    #         list_data = datahandle.handleList(pdata)
    #         self.ProgrameList.SetObjects(list_data)
    #     #gen.IsItemRunChanged = False

    def OnOpenLogFile(self,event):
        LoadLog.LogMsg(gen.logger.info,u"打开日志文件%s" % gen.LOGFILE)
        try:
            subprocess.Popen("C:\\windows\\system32\\notepad.exe %s" % gen.LOGFILE, shell=True)
        except:
            LoadLog.LogMsg(gen.logger.warning,u"打开日志文件%s 失败" % gen.LOGFILE)

    def OnHelp(self,event):
        html = HtmlDocDlg(None)
        html.ShowModal()
        html.Destroy()


class EventSettingMenuAndLog(object):
    def __init__(self,viewbtn,stopbtn,clearbtn,cTextCrtl,IntervalBox):
        self.viewbtn = viewbtn
        self.stopbtn = stopbtn
        self.clearbtn = clearbtn
        self.IntervalBox = IntervalBox
        self.cTextCrtl = cTextCrtl
        self.f = HandleSetting(gen.CONF_FILE)

    def OnViewLog(self,event):
        gen.console_switch = True
        gen.logswitch = True
        self.f.WriteSingleConf("log","enable_console_show","True")
        self.f.WriteSingleConf("log","enable_log","True")
        self.viewbtn.Disable()
        self.stopbtn.Enable()

    def OnStopLog(self,event):
        gen.console_switch = False
        self.f.WriteSingleConf("log","enable_console_show","False")
        self.viewbtn.Enable()
        self.stopbtn.Disable()

    def OnClearLog(self,event):
        self.cTextCrtl.SetValue("")

    def OnClearMax(self,event):
        if self.IntervalBox.GetValue() in gen.SAMPLELIST:
            gen.MSG_MAX =  self.IntervalBox.GetValue()
            f = HandleSetting(gen.CONF_FILE)
            f.WriteSingleConf("log","msg_max",gen.MSG_MAX)
            LoadLog.LogMsg(gen.logger.info,u"更新自动清空控制台的字节大小为%s" % gen.MSG_MAX)

    def OnSettingUI(self,event):
        LoadLog.LogMsg(gen.logger.info,u"打开设置面板")
        if  os.path.exists(gen.CONF_FILE) is  True:
            try:
                f = HandleSetting(gen.CONF_FILE)
                configdict = f.ReadConfFile()
            except:
                configdict = gen.DEFAULT_CONFIG_DICT
        else:
            configdict = gen.DEFAULT_CONFIG_DICT

        dlg = settingDlg(u"设置",configdict)
        dlg.Center()
        if dlg.ShowModal() == wx.ID_OK:
            newConfDict = dlg.SetUI.GenerateConfDict()
            #print newConfDict
            f = HandleSetting(gen.CONF_FILE,newConfDict)
            f.WriteConfFile()
            gen.CONF_DICT = newConfDict
            #print newConfDict
            self.UpdateConfData()
            LoadLog.LogMsg(gen.logger.info,u"更新设置面板的数据")

            if gen.CONF_DICT["log"]["enable_console_show"] is True:
                self.viewbtn.Disable()
                self.stopbtn.Enable()
            else:
                self.viewbtn.Enable()
                self.stopbtn.Disable()

            #print gen.LOOP_TIME
        dlg.Destroy()

    def UpdateConfData(self):
        gen.LOOP_TIME = gen.CONF_DICT["monitor"]["round_robin_scheduling"] * 1000
        gen._filedata = gen.CONF_DICT["monitor"]["data_file"]
        gen.CPU_LOOP_TIME = gen.CONF_DICT["monitor"]["cpu_scheduling"] * 1000
        gen.MEMORY_LOOP_TIME = gen.CONF_DICT["monitor"]["memory_scheduling"] * 1000
        gen.CPU_MON = gen.CONF_DICT["monitor"]["enable_monitor_cpu"]
        gen.MEMORY_MON = gen.CONF_DICT["monitor"]["enable_monitor_memory"]
        gen.logswitch = gen.CONF_DICT["log"]["enable_log"]
        gen.console_switch =  gen.CONF_DICT["log"]["enable_console_show"]
        gen.LOGFILE = gen.CONF_DICT["log"]["log_file"]
        gen.LOG_MAX_BYTES = gen.CONF_DICT["log"]["log_size"] * 1024 * 1024
        gen.BACKUP_COUNT = gen.CONF_DICT["log"]["log_leave"]
        gen.MSG_MAX = gen.CONF_DICT["log"]["msg_max"]
        print type(gen.MSG_MAX)
        gen.FILE_LOG_LEVEL =  gen.CONF_DICT["log"]["log_level"]
        gen.level = gen.LEVELS.get(gen.FILE_LOG_LEVEL,logging.NOTSET)
        gen.CONSOLE_LOG_LEVEL = gen.CONF_DICT["log"]["console_level"]


    ###这里搜索没什么用，以后扩展可能用到吧
    def FindString(self,findString):
        #self.readFindFlags()
        ##大小写敏感匹配检测
        FileContents = self.cTextCrtl.GetValue()
        #findString,FileContents = self.StrmatchCase(findString)
        ##获取文本的选择范围，返回一个字节point位置的元组
        selectPoint = self.cTextCrtl.GetSelection()
        ##如果没有选取文本范围，默认 selectPoint 返回元组的两个数是相等的，也就是等下光标的插入点
        ##如果选取了范围，selectPoint返回元组的两人个数是不相等的
        if selectPoint[0] != selectPoint[1]:
            startFindAt = max(selectPoint)  ##设置查找点 startFindAt 为元组最大的数
        else:
            startFindAt = self.cTextCrtl.GetInsertionPoint()  ##设置开始查找点为光标插入点
        if startFindAt == self.cTextCrtl.GetLastPosition():  ##如果查找点为尽头，重置为0
            startFindAt = 0
        ##开始查找指定的字符
        foundStr = FileContents.find(findString,startFindAt)
        if foundStr != -1:
            ##如果找到，求出字符的最后位置
            EndStr = len(findString) + foundStr
            ##设置文本选取范围
            self.cTextCrtl.SetSelection(EndStr,foundStr)
            ##设置文本选取范围的focus
            self.cTextCrtl.SetFocus()
            return True
        else:
            return False


