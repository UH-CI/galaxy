import sys
import os
from miniapp import *
from third_party.slurm.database.util import * 


def __main__():
    if len(sys.argv) != 3:
        print >> sys.stderr, "USAGE: %s "<partition and account>" <user id number>" %(sys.argv[0])
        return
    ini_path = None
    for guess in DEFAULT_INIS:
        ini_path = os.path.join(GALAXY_ROOT_DIR, guess)
        if os.path.exists(ini_path):
            break
    if ini_path and not os.path.isabs(ini_path):
        ini_path = os.path.join(GALAXY_ROOT_DIR, ini_path)
    account_partition, userid= sys.argv[1:]    
    account_partition = account_partition.replace("__sq__", "'")
    account_partition = eval("{" + account_partition + "}")
    app = MiniApplication(global_conf={"__file__": ini_path}, ini_file=ini_path, init_section="app:%s"%(DEFAULT_INI_APP))

    try:
        print "Attempting to set slurm submission account to '%s' and partition to '%s'"%( account_partition['account'], account_partition['partition'] )
        setSlurmAccountandPartition(app.model.context, userid, account_partition)
        print "Slurm submission account and partition have been set to '%s' and '%s'"%( account_partition['account'], account_partition['partition'] )
    except:
        print >> sys.stderr, "An error occurred while trying to set the slurm submission account and partition"
    app.object_store.shutdown()
    


if __name__ == '__main__':
    __main__()
