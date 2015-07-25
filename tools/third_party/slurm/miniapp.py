import sys
import os

#new_path = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.pardir, os.pardir ) )



GALAXY_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", '..'))
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
    def __init__( self, **kwargs ):
        os.chdir(GALAXY_ROOT_DIR)
        self.name = 'galaxy'
        self.new_installation = False
        # Read config file and check for errors
        self.config = config.Configuration( **kwargs )
        self._configure_object_store( fsmon=False )        
        config_file = kwargs.get( 'global_conf', {} ).get( '__file__', None )
        self._configure_models( check_migrate_databases=False, check_migrate_tools=False, config_file=config_file )



