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
    app = MiniApplication(global_conf={"__file__": ini_path}, ini_file=ini_path, init_section="app:%s"%(DEFAULT_INI_APP))
    try:
        print "Attempting to set slurm submission partition to '%s'"%(partition)
        setSlurmPartition(app.model.context, userid, partition)
        print "Slurm submission partition has been set to '%s'"%(partition)
    except:
        print >> sys.stderr, "An error occurred while trying to set the slurm submission partition"
    app.object_store.shutdown()
    


if __name__ == '__main__':
    __main__()
