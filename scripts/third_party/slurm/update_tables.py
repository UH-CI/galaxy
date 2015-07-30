#!/bin/env python

import yaml
import sys
import os
GALAXY_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
GALAXY_LIB_DIR = os.path.join(GALAXY_ROOT_DIR, "lib")
sys.path.insert( 0, GALAXY_LIB_DIR)
from third_party.miniapp import *


# def setSlurmPartition(sa_session, usrid, partition):
#     if partition == 'DEFAULT':
#         sql = """UPDATE galaxy_user_slurm_partition SET selected = 0 WHERE user_id = :usrid;"""
#         sa_session.execute(sql, {'usrid' : usrid})
#     else:
#         sql = """SELECT id FROM slurm_partition WHERE name = :lbl;"""
#         result = sa_session.execute(sql, {'lbl': partition})
#         accountid = result.fetchone()[0]
#         result.close()
#         sql = """UPDATE galaxy_user_slurm_partition SET selected = 0 WHERE user_id = :usrid;"""
#         sa_session.execute(sql, {'usrid':usrid})
#         sql = """UPDATE galaxy_user_slurm_partition SET selected = 1 WHERE user_id = :usrid AND partition_id = :accnt;"""
#         sa_session.execute(sql, {'usrid' : usrid, 'accnt' : accountid})


def update_account_table(app, slurminfo):
    accnt_map = dict(app.contect.execute("""select name, id from slurm_account;"""))
    for accnt in slurminfo['accounts']:
        if accnt not in accnt_map:
            app.contect.execute("""INSERT INTO slurm_account(name) VALUES(:name);""",  {'name': accnt})
    accnt_map = dict(app.contect.execute("""select name, id from slurm_account;"""))
    for k, v in slurminfo['usr_to_accnt'].iteritems():
        v = [accnt_map[i] for i in v]
        

def convert_username_to_userid(app, slurminfo):
    usermap = slurminfo['usr_to_accnt']
    usrselect = dict()
    for r in app.contect.execute("""select id, username from galaxy_user;"""):
        if r.username in usermap:
            usrselect[r.id] = usermap[r.username]
    return usrselect


def __main__():
    if len(sys.argv) != 3:
        print >> sys.stderr, "USAGE: %s <account> <user id number>" %(sys.argv[0])
        return
    ini_path = None
    for guess in DEFAULT_INIS:
        ini_path = os.path.join(GALAXY_ROOT_DIR, guess)
        if os.path.exists(ini_path):
            break
    if ini_path and not os.path.isabs(ini_path):
        ini_path = os.path.join(GALAXY_ROOT_DIR, ini_path)
    account, userid= sys.argv[1:]
    app = MiniApplication(global_conf={"__file__": ini_path}, ini_file=ini_path, init_section="app:%s"%(DEFAULT_INI_APP))
    try:
        print "Attempting to set slurm submission account to '%s'"%(account)
        setSlurmAccount(app.model.context, userid, account)
        print "Slurm submission account has been set to '%s'"%(account)
    except:
        print >> sys.stderr, "An error occurred while trying to set the slurm submission account"
    app.object_store.shutdown()


if __name__ == '__main__':
    __main__()
