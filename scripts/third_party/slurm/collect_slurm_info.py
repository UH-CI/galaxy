#!/bin/env python
import sys
import subprocess
import yaml
import cStringIO as StringIO
from collections import defaultdict

"""
ASSUMPTIONS:
1. all nodename start with [^-]+-
2. the node and partition lines start with nodename and partitionname
3. the config file has realmemory and procs defined for the nodes
4. the slurm.conf is located at /etc/sysconfig/slurm/slurm.conf
"""


lines  = [ dict([ (i.split("=")[0].lower(), i.split("=")[1], ) for i in l.strip().split()]) for l in open("/etc/sysconfig/slurm/slurm.conf") if l.startswith("PartitionName") or l.startswith("NodeName")]

#-nodes = dict([ ( "-".join(i['nodename'].split("[")[0].split("-")[:-1]), (i['procs'], i['realmemory'],) , )  for i in lines if "nodename" in i and 'realmemory' in i and 'procs' in i ])

nodes = defaultdict(tuple)
for i in lines:
    if "nodename" in i and 'realmemory' in i and 'procs' in i :    
        name =  "-".join(i['nodename'].split("[")[0].split("-")[:-1])
        info = (i['procs'], i['realmemory'],)
        if name in nodes:
            if int(nodes[name][0]) > int(info[0]) or float(nodes[name][1]) > float(info[1]):
                nodes[name] = info
        else:
            nodes[name] = info

# {'corespersocket': '10',
#   'nodename': 'prod2-[0001-0176]',
#   'procs': '20',
#   'realmemory': '129000',
#   'sockets': '2',
#   'state': 'UNKNOWN',
#   'threadspercore': '1'},

partitions = dict([ (i['partitionname'] , ( set(i.get('allowaccounts', "ALL",).split(",") ), i['maxtime'], list(nodes["-".join(i['nodes'].split("[")[0].split("-")[:-1])]), i.get('maxmempercpu', "10000000"), ), )  for i in lines if "partitionname" in i and 'state' in i and i['state'] == 'UP'])

 # {'allowaccounts': 'longrun',
 #  'default': 'NO',
 #  'defaulttime': '5:00',
 #  'defmempercpu': '3250',
 #  'maxmempercpu': '65500',
 #  'maxnodes': '1',
 #  'maxtime': '60:00',
 #  'nodes': 'prod2-sb-[0001-0002]',
 #  'partitionname': 'actest.q',
 #  'preemptmode': 'requeue',
 #  'priority': '10',
 #  'state': 'UP'}]

# collect the account to user mapping
child = subprocess.Popen(str("""sacctmgr -n  show associations format=Account%-30,User%-64"""),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         universal_newlines=True,
                         shell=(sys.platform!="win32"))

sout, serr = child.communicate()
soutfp = StringIO.StringIO(sout)
accountmap = defaultdict(set)
usertoaccount = defaultdict(list)
accountlist = set()
for l in soutfp:
    try:
        account, user = l.split()
    except:
        continue
    accountlist.add(account)
    usertoaccount[user].append(account)
    for k, p in partitions.iteritems():
        if 'ALL' in p[0] or account in p[0]:
            accountmap[account].add(k)


accountlist = list(accountlist)
accountmap  = dict( [ (k, list(v),) for k, v in accountmap.iteritems()])
usertoaccount = dict(usertoaccount)

partitions_clean = dict()
for k, v in partitions.iteritems():
    v = list(v)[1:]
    if v[0].count(":") == 2:
        v[0] = ":".join(v[0].split(":")[:-1])
    else:
        v[0] = "00:%s"%(v[0].split(":")[0])
    partitions_clean[k] = v

partitions = partitions_clean
with open("slurm_partition_info.yml", "w") as o:
    print >> o, yaml.dump(dict(partitions = partitions, accountinfo = accountmap, usr_to_accnt = usertoaccount, accounts = accountlist))


