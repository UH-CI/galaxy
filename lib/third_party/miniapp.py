import sys
import os
import logging

#new_path = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.pardir, os.pardir ) )

GALAXY_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GALAXY_LIB_DIR = os.path.join(GALAXY_ROOT_DIR, "lib")
sys.path.insert( 0, GALAXY_LIB_DIR)
DEFAULT_INI_APP = "main"
DEFAULT_INIS = ["config/galaxy.ini", "universe_wsgi.ini", "config/galaxy.ini.sample"]


from galaxy import eggs
import galaxy.model
import pkg_resources
from galaxy import config
from galaxy.util.properties import load_app_properties

class MiniApplication( object, config.ConfiguresGalaxyMixin ):
    """
    This is just a quick/dirty way to get us access to the database managed by galaxy.  We end up creating
    a partial instance of the galaxy Application which configures the models, which in turns opens up a connection to the database.
    """
    def __init__( self, config_file, ini_section= "app:%s"%(DEFAULT_INI_APP) ):
        logging.raiseExceptions = False
        os.chdir(GALAXY_ROOT_DIR)
        self.name = 'galaxy'
        self.new_installation = False
        kwds = dict( ini_file=config_file,  ini_section="app:%s"%(DEFAULT_INI_APP), )
        kwds = load_app_properties(kwds = kwds, ini_file = config_file)
        print config_file
        self.config = config.Configuration( global_conf={'__file__' : config_file}, **kwds )
        self._configure_object_store( fsmon=False )       
        self._configure_models( check_migrate_databases=False, check_migrate_tools=False, config_file=config_file )
