#coding:utf-8
import logging
import logging.config
import logging.handlers
import time
import idDefine as gen
import wx

class LogConsoleHandler(logging.StreamHandler):
    def __init__(self, textctrl):
        logging.StreamHandler.__init__(self)
        self.textctrl = textctrl

    def emit(self, record):
        #msg = self.format(record)
        #self.textctrl.AppendText(msg + "\n")
        #print gen.MSG_MAX
        if len(self.textctrl.GetValue()) > gen.MSG_MAX:
            self.textctrl.SetValue('')

        if gen.console_switch == True:
            level = gen.LEVELS.get(gen.CONSOLE_LOG_LEVEL,logging.NOTSET)
            if record.levelno < level:
                return
            tstr = time.strftime('%Y-%m-%d_%H:%M:%S.%U')
            self.textctrl.AppendText("[%s]--[%s]:    %s\n"%(tstr,record.levelname,record.getMessage()))
            self.flush()


def LogMain():
    dictLogConfig = {
        "version":1,
        "handlers":{
                    "file":{
                        "class":"logging.handlers.RotatingFileHandler",
                        "formatter":"myFormatter",
                        "filename": gen.LOGFILE,
                        "maxBytes": gen.LOG_MAX_BYTES,
                        "backupCount": gen.BACKUP_COUNT,
                        },
                    "consoleHandler":{
                        "class":"logging.StreamHandler",
                        "formatter":"myFormatter"
                        }
                    },
        "loggers":{
            "ProMonitor":{
                "handlers":["file", "consoleHandler"],
                "level":gen.level
                }
            },
        "formatters":{
            "myFormatter":{
                "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            }
        }
    logging.config.dictConfig(dictLogConfig)
    #logger = logging.getLogger("wxApp")
    #handler = logging.handlers.RotatingFileHandler(gen.LOGFILE,maxBytes=10000,backupCount=5,)
    #logger.addHandler(handler)

    LogMsg(gen.logger.debug,u"加载日志功能函数")

def LogMsg(loglevel,msg):
    if gen.logswitch is True:
        loglevel(msg)