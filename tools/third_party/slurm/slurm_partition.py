import sys
import os

GALAXY_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
GALAXY_LIB_DIR = os.path.join(GALAXY_ROOT_DIR, "lib")
sys.path.insert( 0, GALAXY_LIB_DIR)

from third_party.miniapp import *
from third_party.slurm.database.util import *

def __main__():
    if len(sys.argv) != 3:
        print >> sys.stderr, "USAGE: %s <partition> <user id number>" %(sys.argv[0])
        return
    ini_path = None
    for guess in DEFAULT_INIS:
        ini_path = os.path.join(GALAXY_ROOT_DIR, guess)
        if os.path.exists(ini_path):
            break
    if ini_path and not os.path.isabs(ini_path):
        ini_path = os.path.join(GALAXY_ROOT_DIR, ini_path)
    partition, userid= sys.argv[1:]    
    app = MiniApplication(config_file=ini_path)
    trans = app.model.context.begin()
    o = open(sys.argv[3], "w")
    try:
        print >> o,  "Attempting to set slurm submission partition to '%s'"%(partition)
        setSlurmPartition(app.model.context, userid, partition)
        print >> o ,"Slurm submission partition has been set to '%s'"%(partition)
        trans.commit()
    except:
        trans.rollback()
        print >> o, "An error occurred while trying to set the slurm submission partition"
    app.object_store.shutdown()
    app.model.context.close()


if __name__ == '__main__':
    __main__()
