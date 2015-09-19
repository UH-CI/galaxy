#!/bin/env python

import yaml
import sys
import os
GALAXY_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
GALAXY_LIB_DIR = os.path.join(GALAXY_ROOT_DIR, "lib")
sys.path.insert( 0, GALAXY_LIB_DIR)
from third_party.miniapp import *


def account_to_partition(app, slurminfo):
    partition_map = dict(app.model.context.execute("""select name, id from slurm_partition;""").fetchall())
    accnt_map = dict(app.model.context.execute("""select name, id from slurm_account;""").fetchall())
    #trans = app.model.context.begin()
    app.model.context.execute("""DELETE FROM slurm_partition_to_account;""")
    idx = 1
    for k, v in slurminfo['accountinfo'].iteritems():
        for p in v:
            app.model.context.execute("""INSERT INTO slurm_partition_to_account(id, account_id, partition_id) VALUES(:num, :accid, :partid);""",  dict(num = idx, partid= partition_map[p], accid= accnt_map[k]) )      
            idx += 1
    #trans.commit()


def update_user_slurm_accounts(app, usrselect):
    for r in app.model.context.execute("""SELECT account_id, user_id FROM galaxy_user_slurm_account;"""):
        if r.user_id not in usrselect or r.account_id not in usrselect[r.user_id]: 
            app.model.context.execute("""DELETE FROM galaxy_user_slurm_account WHERE account_id = :accntid AND user_id = :usrid;""", dict(accntid = r.account_id, usrid = r.user_id) )        
    for usrid, accnts in usrselect.iteritems():
        for accnt in accnts:
            r = app.model.context.execute("""SELECT id FROM galaxy_user_slurm_account WHERE account_id=:accnt AND user_id = :usrid LIMIT 1;""", dict(accnt = accnt, usrid = usrid) )
            if r.rowcount == 0:
                app.model.context.execute("""INSERT INTO galaxy_user_slurm_account(account_id, user_id, selected) VALUES(:accid, :usrid, :sel);""", dict(accid = accnt, usrid = usrid, sel = False) )



def update_user_slurm_partitions(app):
#slurm_partition_to_account
    for r in app.model.context.execute("""SELECT account_id, user_id FROM galaxy_user_slurm_account;"""):
        for pa in app.model.context.execute("""SELECT account_id, partition_id FROM slurm_partition_to_account WHERE account_id = :accntid;""", dict(accntid = r.account_id)):
            rr = app.model.context.execute("""SELECT id FROM galaxy_user_slurm_partition WHERE partition_id=:partid AND user_id = :usrid LIMIT 1;""", dict(partid = pa.partition_id, usrid = r.user_id) )
            if rr.rowcount == 0:
                app.model.context.execute("""INSERT INTO galaxy_user_slurm_partition(partition_id, user_id, selected) VALUES(:partid, :usrid, :sel);""", dict(partid = pa.partition_id, usrid = r.user_id, sel = False) )
    for r in app.model.context.execute("""SELECT partition_id, user_id FROM galaxy_user_slurm_partition;"""):
        rr = app.model.context.execute("""SELECT account_id FROM slurm_partition_to_account WHERE partition_id=:partid;""", dict(partid = r.partition_id) )
        if rr.rowcount == 0:
            app.model.context.execute("""DELETE FROM galaxy_user_slurm_partition WHERE partition_id = :partid AND user_id = :usrid;""", dict(partid = r.partition_id, usrid = r.user_id) )
        else:
            # if the partition exists, with some account(s). We need to verify that the user is in one of those accounts.
            rr = app.model.context.execute("""SELECT user_id FROM galaxy_user_slurm_account WHERE user_id = :usrid AND account_id IN :accntid LIMIT 1;""", dict(usrid = r.user_id, accntid = tuple([i[0] for i in rr.fetchall()])) )



def update_partition_table(app, slurminfo):
    partition_map = dict( [ (i.name, i.id,) for i in  app.model.context.execute("""select name, id from slurm_partition;""")])
    for partition, params in slurminfo['partitions'].iteritems():
        maxtime  = params[0]
        maxcpus = int(params[1][0])
        ram_per_cpu = int(params[1][1]) / int(params[1][0])
        if partition not in partition_map:
            app.model.context.execute("""INSERT INTO slurm_partition(name, max_time, max_cpus, ram_per_cpu) VALUES(:name, :max_time, :max_cpus, :ram_per_cpu);""",  {'name': partition, 'max_time': maxtime, 'max_cpus': maxcpus, 'ram_per_cpu': ram_per_cpu })
        else:
            app.model.context.execute("""UPDATE slurm_partition SET max_time=:max_time,max_cpus=:max_cpus,ram_per_cpu=:rpc WHERE name = :partition;""", dict(max_time=maxtime, max_cpus=maxcpus, rpc=ram_per_cpu, partition=partition))


def update_account_table(app, slurminfo, usrselect):
    accnt_map = dict(app.model.context.execute("""select name, id from slurm_account;""").fetchall())
    for accnt in slurminfo['accountinfo'].iterkeys():
        if accnt not in accnt_map:
            app.model.context.execute("""INSERT INTO slurm_account(name) VALUES(:name);""",  {'name': accnt})
    accnt_map = dict(app.model.context.execute("""select name, id from slurm_account;""").fetchall())
    
    for k, v in usrselect.iteritems():
        usrselect[k] = set([accnt_map[i] for i in v])
        

def convert_username_to_userid(app, slurminfo):
    usermap = slurminfo['usr_to_accnt']
    usrselect = dict()
    for r in app.model.context.execute("""select id, username from galaxy_user;"""):
        if r.username in usermap:
            usrselect[r.id] = usermap[r.username]
    return usrselect


def main():
    if len(sys.argv) != 2:
        print >> sys.stderr, "USAGE: %s <slurm yaml>" %(sys.argv[0])
        return
    ini_path = None
    for guess in DEFAULT_INIS:
        ini_path = os.path.join(GALAXY_ROOT_DIR, guess)
        if os.path.exists(ini_path):
            break
    if ini_path and not os.path.isabs(ini_path):
        ini_path = os.path.join(GALAXY_ROOT_DIR, ini_path)

    ymlfile = os.path.abspath(sys.argv[1])
    app = MiniApplication(config_file=ini_path)
    trans = app.model.context.begin() 
    try:
        print >> sys.stderr, "Begin slurm user information update process"
        slurminfo = yaml.load(open(ymlfile))
        usrselect = convert_username_to_userid(app, slurminfo)
        update_account_table(app, slurminfo, usrselect)
        update_partition_table(app, slurminfo)
        account_to_partition(app, slurminfo)
        update_user_slurm_accounts(app, usrselect)
        update_user_slurm_partitions(app)
        trans.commit()
        print >> sys.stderr, "Slurm information has been updated in the galaxy database"
    except:
        trans.rollback()
        print >> sys.stderr, "An error occurred while trying to update slurm information in galaxy"
    app.object_store.shutdown()
    app.model.context.close()


if __name__ == '__main__':
    main()
