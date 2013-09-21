#coding:utf-8

import ConfigParser
from ConfigParser import SafeConfigParser
config = SafeConfigParser()

class HandleSetting(object):
    def __init__(self,configfile,inidict=None):
        self.configfile  = configfile
        self.inidict = inidict

    def ReadConfFile(self):
        config.read(self.configfile)
        cdict = {}
        for section in config.sections():
            cdict[section] = {}
            for option in config.options(section):
                if config.get(section, option) in ["True","true","False","false"]:
                    cdict[section][option] = config.getboolean(section, option)
                elif config.get(section, option).isdigit():
                    cdict[section][option] = config.getint(section, option)
                else:
                    cdict[section][option] = config.get(section, option)
        return cdict

    def ReadSingleConf(self,section,option):
        f = open(self.configfile)
        f.seek(0)
        config.readfp(f)
        f.close()
        return config.getboolean(section, option)

    def WriteSingleConf(self,section,option,value):
        f = open(self.configfile,'w')
        #f.seek(0)
        #config.readfp(f)
        config.set(section,option,value)
        config.write(f)
        f.close()

    def WriteConfFile(self):
        for section,options in self.inidict.items():
            for key,value in options.items():
                try:
                    config.set(section,key,str(value))
                except ConfigParser.NoSectionError:
                    config.add_section(section)
                    self.WriteConfFile()
        with open(self.configfile,'w') as f:
            config.write(f)

if __name__ == "__main__":
    f = HandleSetting("setting.ini")
    iniDict =  f.ReadConfFile()
    print iniDict["base"]["startup"]
    print iniDict["base"]["autoupdate"]
    print iniDict["log"]["log_size"]
    print iniDict

    f2 = HandleSetting("setting2.ini",iniDict)
    f2.WriteConfFile()

# f = open("setting.ini",'r')
# f.seek(0)
# scp.readfp(f)  ##读取文件
# for section in scp.sections():  ## scp.sections 为全部 section, 进入循环读取
#     print "[%s]\n" % section
#     options = scp.options(section)   ## 所有的option
#     for option in options:
#          ## scp.get(section, option) 为value, 此处打印所有的option 和 value
#         print "%s: %s" %(option,scp.get(section,option))
#     print "--" * 20
#
# ## 单独操作读取配置文件
# print scp.get('base','startup')
# print scp.get('base','tray_minimize')
# print scp.get('base','autoupdate')