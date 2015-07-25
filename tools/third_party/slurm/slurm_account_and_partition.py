import sys
import os
from miniapp import *
from third_party.slurm.database.util import * 


def __main__():
    if len(sys.argv) != 3:
        print >> sys.stderr, "USAGE: %s '<partition;account>' <user id number>" %(sys.argv[0])
        return
    ini_path = None
    for guess in DEFAULT_INIS:
        ini_path = os.path.join(GALAXY_ROOT_DIR, guess)
        if os.path.exists(ini_path):
            break
    if ini_path and not os.path.isabs(ini_path):
        ini_path = os.path.join(GALAXY_ROOT_DIR, ini_path)
    account_partition, userid= sys.argv[1:]    
    app = MiniApplication(global_conf={"__file__": ini_path}, ini_file=ini_path, init_section="app:%s"%(DEFAULT_INI_APP))

    #try:
    setSlurmAccountandPartition(app.model.context, userid, account_partition)
    #except:
    #    pass

    print app.model.context
    app.object_store.shutdown()
    


if __name__ == '__main__':
    __main__()
