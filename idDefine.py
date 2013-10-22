#coding:utf:8
import os
import logging.handlers
import logging
from SettingData import  HandleSetting


ID_VIEW = 1000
ID_START = 1001
ID_STOP = 1002
ID_MONITOR = 1003
ID_STOP_MONITOR = 1004
ID_REFRESH_MONITOR = 1005
ID_REFERSH_INTERVA = 1006
ID_UNSELECTALL = 1007
ID_IMPORT = 1008
ID_EXPORT = 1009
ID_SELECTCLEAR = 1010
ID_START = 1011
ID_STOP = 1012
ID_RESTART = 1013
ID_MONITOR = 1014
ID_NOMONITOR = 1015
ID_DATA = 1016
ID_DEFAULT = 1017
ID_STARTUP = 1018
ID_MINICON = 1019
ID_AUTOUPDATE = 1020
ID_CONSOLE_SHOW = 1021
ID_LOG_SHOW = 1022
ID_MONITOR_CPU = 1023
ID_MONITOR_MEMORY = 1024
ID_SHOW_WIN = 1025
ID_LOG_FILE = 1026
ID_OPERATOR = 1027

operatorDict = {
    u"等于": "=",
    u"小于": "<",
    u"大于": ">",
    u"小于或等于": "<=",
    u"大于或等于": ">=",
    u"不等于": "!="
}

DEFAULT_CONFIG_DICT = {
	'base' : {
		'autoupdate' : False,
		'tray_minimize' : False,
		'startup' : False
	},
	'monitor' : {
		'round_robin_scheduling' : 20,
		'enable_monitor_memory' : False,
		'data_file' : 'data\data.json',
		'enable_monitor_cpu' : False,
		'cpu_scheduling' : 30,
		'memory_scheduling' : 60
	},
	'log' : {
		'enable_console_show' : False,
		'enable_log' : False,
        'log_leave' : 3,
		'log_size' : 3,
		'log_file' : 'logs\pro_monitor.log',
        'msg_max' : 10240,
		'console_level' : 'info',
        'log_level' : 'debug'
	}
}
LEVELS = {
    'debug':logging.DEBUG,
    'info': logging.INFO,
    'warning':logging.WARNING,
    'error':logging.WARNING,
    'critical':logging.CRITICAL
}
SAMPLELIST = ['1024', '5120', '8190', '12040', '20480']

CONF_FILE = "setting.ini"
HTMLDOC = "doc\index.html"
CUR_PATH = os.path.split(__file__)[0]
IsItemChanged = False
IsRunStatusChanged = False
LoadDefaultConf = False
SPLASH_TIME = 5000

def getConfDict():
    import os
    #print "********** Recall Data ***********"
    if os.path.exists(CONF_FILE):
        CONF_DICT = HandleSetting(CONF_FILE).ReadConfFile()
    else:
        CONF_DICT = DEFAULT_CONFIG_DICT
    return CONF_DICT

CONF_DICT = getConfDict()

LOOP_TIME = CONF_DICT["monitor"]["round_robin_scheduling"] * 1000
_filedata = CONF_DICT["monitor"]["data_file"]
CPU_LOOP_TIME = CONF_DICT["monitor"]["cpu_scheduling"] * 1000
MEMORY_LOOP_TIME = CONF_DICT["monitor"]["memory_scheduling"] * 1000

CPU_MON = CONF_DICT["monitor"]["enable_monitor_cpu"]
MEMORY_MON = CONF_DICT["monitor"]["enable_monitor_memory"]

logswitch = CONF_DICT["log"]["enable_log"]
#logswitch = True
console_switch =  CONF_DICT["log"]["enable_console_show"]
#console_switch = True
LOGFILE = CONF_DICT["log"]["log_file"]
LOG_MAX_BYTES = CONF_DICT["log"]["log_size"] * 1024 * 1024
BACKUP_COUNT = CONF_DICT["log"]["log_leave"]
FILE_LOG_LEVEL =  CONF_DICT["log"]["log_level"]
CONSOLE_LOG_LEVEL = CONF_DICT["log"]["console_level"]
MSG_MAX = CONF_DICT["log"]["msg_max"]


level = LEVELS.get(FILE_LOG_LEVEL,logging.NOTSET)

logger = logging.getLogger("ProMonitor")
handler = logging.handlers.RotatingFileHandler(LOGFILE,maxBytes=LOG_MAX_BYTES,backupCount=BACKUP_COUNT,)
logger.addHandler(handler)

#PDATA = {}
allProNum = 0
monProNum = 0
runProNum = 0
MEMORY = ""
CPU = ""
