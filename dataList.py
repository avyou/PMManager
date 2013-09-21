#coding:utf-8
import codecs
import os
import json
import idDefine as gen
import logging
import LogOutput as LoadLog


class ListObj(object):
    def __init__(self, id,kid, name, programe, logfile,status,monitor,operator,processNum,runAs,note):
        """Constructor"""
        self.id = id
        self.kid = kid
        self.name = name
        self.programe = programe
        self.logfile = logfile
        self.status = status
        self.monitor = monitor
        self.operator = operator
        self.processNum = processNum
        self.runAs = runAs
        self.note = note

class DataHandle(object):
    def __init__(self,filename):
        self.filename = filename
    ##读数据操作
    def ReadData(self):
        try:
            # if gen.logswitch is True:
            #     logger = logging.getLogger("wxApp")
            #     logger.info(u"读取数据文件，返回python字典.")
            LoadLog.LogMsg(gen.logger.info,u"读取数据文件，返回数据字典.")
            with codecs.open(self.filename,'r',"utf-8") as f:
                try:
                    self.pdata = json.loads(f.read(),"utf-8")
                except (TypeError, ValueError) as err:
                    self.pdata = None
        except:
            self.pdata=None
        return self.pdata

    ##写数据操作
    def WriteData(self,pdata):
        try:
            with codecs.open(self.filename,"w","utf-8") as f:
                try:
                    jdata = json.dumps(pdata,indent=2,ensure_ascii=False)
                    LoadLog.LogMsg(gen.logger.debug,u"转化为 json 数据：%s" % jdata)
                    f.write(jdata)
                    LoadLog.LogMsg(gen.logger.info,u"成功将数据写入文件")
                except (TypeError, ValueError) as err:
                    #print u"###保存数据出错,错误信息",err
                    LoadLog.LogMsg(gen.logger.critical,u"保存数据出错,错误信息:%s" %err)
                    return
        except:
            LoadLog.LogMsg(gen.logger.critical,u"保存数据出错,错误信息")
            return

    ############### 数据文件读取数据，以及根据"运行状态"，"监控状态" 的值，显示给列表控件###########
    def handleList(self,update=None):
        if update is not None:
            LoadLog.LogMsg(gen.logger.debug,u"从内存中的获取数据字典")
            self.pdata = update
        else:
            self.pdata = self.ReadData()

        if gen.IsRunStatusChanged == True:
            LoadLog.LogMsg(gen.logger.info,u"编辑发生改变，检测进程数来确定进程状态。")
            LoadLog.LogMsg(gen.logger.debug,u"要处理的字典：%s" % self.pdata)

            for kid in self.pdata.keys():
                ProPath = self.pdata[kid]["programe"]
                ProName = os.path.basename(ProPath)
                if self.pdata[kid]["monitor"] is True:
                    Operator = self.pdata[kid]["operator"]
                    proNum = self.pdata[kid]["processNum"]
                    LoadLog.LogMsg(gen.logger.info,u"%s的进程数: %d" %(ProName, proNum))
                    if self.GetProcessCount(ProName) == 0 :
                       LoadLog.LogMsg(gen.logger.debug,u"改为%s进程的状态为False" %ProName)
                       self.pdata[kid]["status"] = False
                    elif self.OperatorExpress(Operator,ProName,proNum) :
                        LoadLog.LogMsg(gen.logger.debug,u"改为%s进程的状态为True" %ProName)
                        self.pdata[kid]["status"] = True
                    else:
                        self.pdata[kid]["status"] = False
                        LoadLog.LogMsg(gen.logger.debug,u"改为%s进程的状态为False" %ProName)
                else:
                    self.pdata[kid]["status"] = ""
                    LoadLog.LogMsg(gen.logger.debug,u"改为%s进程的状态为空" % ProName)
            gen.IsRunStatusChanged = False

        if self.pdata is not None:
            self.list_data = []
            try:
                for num,kid, in enumerate(sorted(self.pdata)):
                    ldata = self.pdata[kid]
                    programe = os.path.abspath(ldata["programe"])

                    if os.path.isfile(ldata["logfile"]):
                        logfile = os.path.abspath(ldata["logfile"])
                    else:
                        logfile = ldata["logfile"]

                    if ldata["status"] is True:
                         status = u"运行中"
                    elif ldata["status"] is False:
                         status = u"未运行"
                    else:
                         status = ""
                    if ldata["monitor"] is True:
                        monitor = "YES"
                    else:
                        monitor = "NO"
                    if ldata["runAs"] == 0:
                        runAs = u"隐藏"
                    else:
                        runAs = u"显示"

                    operator = gen.operatorDict[ldata["operator"]]
                    ##初始化 ListObj 类的实例，返回控件列表每一项的全局值
                    eachData = ListObj(
                        num+1,ldata["kid"],ldata["name"],programe,logfile,
                        status,monitor,operator,ldata["processNum"],runAs,ldata["note"])
                    ##每一项的值，增加到定义的 list_data 空列表中
                    #print "++++++++++===========",eachData
                    self.list_data.append(eachData)
            except:
                self.list_data = None
                LoadLog.LogMsg(gen.logger.warning,u"返回的数据列表的为None")
        LoadLog.LogMsg(gen.logger.info,u"刷新并返回数据列表")
        return self.list_data

    ################ 将对话框用户输入的值，进行处理然后写入数据文件
    def Add_Edit_Data(self,kid,name,programe,logfile,monitor,operator,processNum,runAs,note):
        ##读取数据
        self.pdata = self.ReadData()

        ##如果数据为空，初始化字典为空
        if self.pdata is  None:
            LoadLog.LogMsg(gen.logger.warning,u"数据文件为空，返回空的字典")
            self.pdata = {}

        ##保存转化整数型的key
        if kid is None:
            LoadLog.LogMsg(gen.logger.debug,u"添加项目，递增得到唯一的kid")
            keys_list = []
            for kid in self.pdata.keys():
                keys_list.append(int(kid))

            ##获取最大的key
            if len(keys_list) == 0:
                kid = "1"
            else:
                max_key = max(keys_list)
            ## 增加的key 值，在最大的值的基础加1,并转换为字符型
                kid = str(max_key + 1)
        # print os.path.relpath(programe)
        # if os.path.dirname(programe) == os.path.dirname(__file__):
        #     print "1111111111111111"
        # print os.path.split(__file__)[0]
        # print os.path.pardir
        # print os.path.relpath("D:\\all_source\\python\\proManager\\demo\\logtest.exe")
        # if "D:\\all_source\\python\\proManager\\demo\\logtest.exe".startswith(os.path.split(__file__)[0]):
        # #if programe.startswith(os.path.split(__file__)[0]):
        #     print "D:\\all_source\\python\\proManager\\demo\\logtest.exe".split(os.path.split(__file__)[0])[1]

        ##如果运行的程序文件在当前目录下，使用相对路径保存
        # if os.path.dirname(programe) == os.path.dirname(__file__):
        #     programe = os.path.basename(programe)

        ##如果运行的程序的目录是当前目录的子目录，使用相对路径
        if str(programe).startswith(gen.CUR_PATH):
            programe = str(programe).split(gen.CUR_PATH+os.path.sep)[1]

        if  os.path.isfile(logfile):
            if str(logfile).startswith(gen.CUR_PATH):
                logfile = str(logfile).split(gen.CUR_PATH+os.path.sep)[1]

        ##添加字典key
        self.pdata[kid] = {}
        self.pdata[kid]["kid"] = kid
        self.pdata[kid]["name"] = name
        self.pdata[kid]["programe"] = programe
        self.pdata[kid]["logfile"] = logfile
        self.pdata[kid]["runAs"] = runAs
        self.pdata[kid]["operator"] = operator
        self.pdata[kid]["processNum"] = processNum
        self.pdata[kid]["status"] = ""
        self.pdata[kid]["monitor"] = monitor
        self.pdata[kid]["note"] = note
        #print u"对话框传入的值======>",kid,name,programe,logfile,note,monitor
        #print u"python字典值: "
        #for key,value in self.pdata.items():
        #    print key,value
        #print "########################################################"
        self.WriteData(self.pdata)

    def GetProcessCount(self,ProName):
        ProName = str(ProName)
        p = os.popen('tasklist /FI "IMAGENAME eq %s"' % ProName)
        LoadLog.LogMsg(gen.logger.debug,u"检查进程列表得到进程数")
        return p.read().count(ProName)

    def OperatorExpress(self,Operator,ProName,proNum):
        if Operator == "=":
            return (self.GetProcessCount(ProName) == proNum)
        elif Operator == "<":
            return (self.GetProcessCount(ProName) < proNum)
        elif Operator == ">":
            return (self.GetProcessCount(ProName) > proNum)
        elif Operator == "<=":
            return (self.GetProcessCount(ProName) <= proNum)
        elif Operator == ">=":
            return (self.GetProcessCount(ProName) >= proNum)
        elif Operator == "!=":
            return (self.GetProcessCount(ProName) != proNum)

if __name__ == "__main__":
    a = DataHandle("json.txt")
    print a.handleList()
