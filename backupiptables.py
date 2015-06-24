#!/usr/bin/python
#coding:utf-8

import paramiko
import socket
import collections
import MySQLdb


def getip(hostname):
    h='%s' %(hostname)
    ip = socket.gethostbyname(h)
    return ip

def getiptables(hostlist):
    username='root'
    password=''
    command="cat /etc/sysconfig/iptables"
    try:
	policydict={}
        for host in hostlist:
	    ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host,22,username,password,timeout=5)
	    stdin,stdout,sterr=ssh.exec_command(command,timeout=10)
	    firewallpolicy=stdout.read()
	    ip=getip(host)
	    if firewallpolicy is not None:
	        policydict[host]={"IP":ip,"iptables":firewallpolicy}
	    else:
		policydict[host]="NULL"
    except Exception as e:
	    print e
    return policydict

def insertdatabase(policydict):
    policydict=getiptables(hostlist)
    #print policydict
    conn=MySQLdb.connect(host="Localhost",user="root",passwd="",db="backupiptables",charset="utf8")
    cursor = conn.cursor()
    for host,value in policydict.items():
	print host
	try:
            status=cursor.execute("select * from iptables where host='%s'" % host)
	    if status == 1:
                sql = "update iptables set host=%s,ip=%s,iptables=%s where host=%s"
		param = (host,value["IP"],value["iptables"],host)
	        n = cursor.execute(sql,param)
    		conn.commit()
	    else:
	        sql = "insert into iptables(host,ip,iptables)  values(%s,%s,%s)" 
		param = (host,value["IP"],value["iptables"])
	        n = cursor.execute(sql,param)
    		conn.commit()
	except Exception as e:
	    print e
    conn.close() 

hostlist=[ "note00" + str(x) for x in range(1,10)] + [ "note0" + str(x) for x in range(10,15)]
insertdatabase(hostlist)
