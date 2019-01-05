# /etc/init.d/mqttfaker.py
### BEGIN INIT INFO
# Provides:          mqttfaker.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    ????
    Created on ??.??.????
    @author: Tobias Badertscher

"""
import sys
import os
import inspect
try:
    from urllib.request import urlopen
except:
    from urllib2 import urlopen
import json
import paho.mqtt.client as mqttc
import time
import random
import copy

SENSOR_IP="192.168.4.10/data.json"
MQTT_SERVER="192.168.4.1"
published_topic={u'data': {u'temperature': {u'data': 30.568182, u'unit': u'C'}, 
                           u'gyro': {u'data': [-140.0, -420.0, 210.0], u'unit': u''}, 
                           u'magneto': {u'data': [187, -605, 155], u'unit': u''}, 
                           u'accel': {u'data': [-18, -19, 1043], u'unit': u''}, 
                           u'humidity': {u'data': 21.092356, u'unit': u'%'}, 
                           u'pressure': {u'data': 968.309998, u'unit': u'hPa'}, 
                           u'version': {u'data': u'0x01010300', u'unit': u''}, 
                           u'cpu_temperature': {u'data': 31.0, u'unit': u'C'},
                           u'fake': {u'data': True, u'unit': u''}}}

published_topic_c={'cpu_temperature':2, 'temperature':2, 'humidity':2, 'pressure':5}


thisModule = sys.modules[__name__]
gitHash=None
pythonVersion=sys.version_info[0:3]
exportPrefix='ex_'
#######################################
#
# helper stuf
#
#######################################
def GetSensorData():
    try:
        srv = urlopen("http://"+SENSOR_IP, timeout=1.5)
        data = json.loads(srv.read())
    except:
        data = FakeData()
    return data
  
def FakeData():
    data = copy.copy( published_topic )
    for k,v in published_topic_c.items():
        # +/- given percentage
        ch_factore = (2*random.random()-1)/100.0*v
        new_val = ch_factore+data['data'][k]['data']
        data['data'][k]['data'] = new_val
    data['data']['fake']['data']=True
    return data

def PublishData(data):
    m = mqttc.Client("DataSource")
    m.connect(MQTT_SERVER)
    for k,v in data['data'].items():
        topic="sensor/%s" % k
        if isinstance(v['data'], list):
            pass
        else:
            #print("Publish %s = %s" % ( topic, v['data']))
            m.publish(topic, v['data'])        
            time.sleep(0.05)
        

#######################################
#
# script functions
#
#######################################
def ex_start(*para):
    '''
    start
    Start polling sensor node and publish stuff to MQTT server.
    '''
    print("Run start")
    while True:
        data=GetSensorData()
        PublishData(data)
        time.sleep(1)
    return


#######################################
#
# Collect all commands in this script.
#
#######################################
def getModuleInfo():
    #print("Items in the current context:")
    exPrefixlen=len(exportPrefix)
    cmds={}
    moduleDoc=""
    for name, item in inspect.getmembers(thisModule):
        if inspect.isfunction(item):
            if exportPrefix == item.__name__[0:exPrefixlen]:
                cmds[item.__name__]=item
        if inspect.ismodule(item):
            moduleDoc=item.__doc__
    return cmds, moduleDoc

def cleanUpTextList(tList):
    '''
    Remove empty lines in a \n separated test list
    '''
    text=[]
    for i in tList:
        i=i.strip()
        if len(i)>0:
            text.append(i)
    return text
#######################################
#
# Usage and main entrance of skript
#
#######################################
def Usage(error=None):
    skriptname=sys.argv[0].split(os.sep)[-1]
    CnCDict, moduleDoc =getModuleInfo()
    sCList  =  list(k for k in  CnCDict.keys() )
    sCList.sort()
    text=cleanUpTextList(moduleDoc.split("\n"))
    cmdStr="command"
    maxCmdLen=len(cmdStr)
    for cmd in sCList:
        maxCmdLen = maxCmdLen if len(cmd)<maxCmdLen else len(cmd)
    commentPos=12
    text.extend([
          "(Git-Hash %s)" % (gitHash) if gitHash is not None else "",
          #"",
          "Comand line:",
          "  %s cmd parameter" % skriptname,
          " "*commentPos+"'cmd' and 'parameter' according to the following list:",
          " "*commentPos+"(Parameters in [xxx] are optional and should - if used - entered without [])",
          ])
    cmdHeader="    command      parameter"
    if pythonVersion[1]>5:
        cmdHeader="    {cmd:{cwidth}} {b}".format(cmd=cmdStr,b="Parameter(s)",cwidth=maxCmdLen+1)
    #text.append(cmdHeader)
    for cmdName in sCList:
        if CnCDict[cmdName].__doc__!=None:
            cmdInfo=cleanUpTextList(CnCDict[cmdName].__doc__.split("\n"))
            cmdName=cmdInfo[0].split()[0].strip()
            para=" ".join(cmdInfo[0].split()[1:])
            if pythonVersion[1]>5:
                text.append("    {a:{cwidth}} {b}".format(a=cmdName,b=para,cwidth=maxCmdLen+1))
            else:
                text.append("    %s %s" % (cmdInfo[0].strip(),cmdInfo[1].strip()))
            if len(cmdInfo)>1:
                for line in cmdInfo[1:]:
                    text.append(" "*commentPos+line.strip())
    res="\n".join(text)
    etext=[]
    if error != None:
        error.insert(0,"ERROR:")
        maxlen=max([len(i) for i in error])
        etext.append("*"*(maxlen+4))
        etext.append("*"*(maxlen+4))
        for i in error:
            etext.append("* "+i+"%s *" % (" "*(maxlen-len(i))))
        etext.append("*"*(maxlen+4))
        etext.append("*"*(maxlen+4))
        print("\n".join(etext))
    print(res)
    sys.exit()

def main():
    if len(sys.argv)<2:
        Usage(["No Command given",])
    cmd=sys.argv[1]
    cmds, moduleDoc = getModuleInfo()
    iCmd='ex_'+cmd
    if iCmd not in cmds:
        Usage()
    cmds[iCmd](sys.argv[2:])

if __name__ == '__main__':
    #main()
    ex_start()
    

