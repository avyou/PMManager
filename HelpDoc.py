#coding:utf-8
import wx
import wx.html
import idDefine as gen
import LogOutput as LoadLog

class HtmlDocDlg(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, u'帮助文档',
                           style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.TAB_TRAVERSAL)
        #panel = wx.Panel(self, -1)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        htmldoc = wx.html.HtmlWindow(self, -1,size=(1000,768))
        try:
            htmldoc.LoadPage(gen.HTMLDOC)
        except:
            LoadLog.LogMsg(gen.logger.warning,u"载入文档出错，请检测文件是否存在或是否有权限读取。")
        vsizer.Add(htmldoc,1,wx.EXPAND)
        self.SetSizerAndFit(vsizer)

if __name__ == '__main__':
    app = wx.App()
    dlg = HtmlDocDlg(None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()