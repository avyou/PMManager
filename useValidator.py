#coding:utf-8
import wx
import os

class InputValidator(wx.PyValidator):# 创建验证器子类
     def __init__(self,flag):
         wx.PyValidator.__init__(self)
         ##传入一个校验的标志
         self.flag = flag

     # def ProList(self):
     #     self.datahandle = DataHandle(gen._filedata)
     #     pdata = self.datahandle.ReadData()
     #     proList = []
     #     for kid in pdata:
     #         proList.append(pdata[kid]["ProName"])
     #     return proList

     def Clone(self):
         return InputValidator(self.flag)

     def Validate(self, win):#1 使用验证器方法
         textCtrl = self.GetWindow()
         text = textCtrl.GetValue()

         if self.flag in ["name_t","fpath_t","logpath_t","save_path_t"] and len(text) == 0:
             wx.MessageBox(u"输入不能不空",u"错误",wx.OK | wx.ICON_ERROR)
             textCtrl.SetBackgroundColour("pink")
             textCtrl.SetFocus()
             textCtrl.Refresh()
             return False
         elif self.flag == "fpath_t" and not (text.upper().endswith(".EXE") or text.upper().endswith(".BAT")) :
             wx.MessageBox(u"输入的程序路径必须为可执行文件",u"错误",wx.OK | wx.ICON_ERROR)
             textCtrl.SetBackgroundColour("pink")
             textCtrl.SetFocus()
             textCtrl.Refresh()
             return False
         elif self.flag in ["fpath_t","logpath_t"] and not os.path.exists(text):
             wx.MessageBox(u"输入的程序路径不存在",u"错误",wx.OK | wx.ICON_ERROR)
             textCtrl.SetBackgroundColour("pink")
             textCtrl.SetFocus()
             textCtrl.Refresh()
             return False
         # elif self.flag == "fpath_t" and text in self.ProList():
         #     wx.MessageBox(u"该项目的进程已经存在",u"错误",wx.OK | wx.ICON_ERROR)

         else:
             textCtrl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
             textCtrl.Refresh()
         return True
     def TransferToWindow(self):
         return True
     def TransferFromWindow(self):
         return True