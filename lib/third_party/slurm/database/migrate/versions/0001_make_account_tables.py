"""
Migration script creates new tables to associate users to slurm accounts
"""
from sqlalchemy import *
from sqlalchemy.orm import *
from migrate import *
from migrate.changeset import *
from galaxy.model.custom_types import *

import datetime
now = datetime.datetime.utcnow

import logging
log = logging.getLogger( __name__ )

metadata = MetaData()


slurm_account = Table( "slurm_account", metadata,
    Column( "id", Integer, primary_key = True ),
    Column( "name", TEXT, default = False  ) )

galaxy_user_slurm_account = Table( "galaxy_user_slurm_account", metadata,
    Column( "id", Integer, primary_key = True ),
    Column( "account_id", Integer, ForeignKey("slurm_account.id"), index = True),
    Column( "user_id", Integer, ForeignKey( "galaxy_user.id" ), index = True ),
    Column( "selected", Boolean, default = False, index = True  ) )
#    Column( "default", Boolean, default = False, index = True  ) )

def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    print __doc__
    metadata.reflect()

    try:
        slurm_account.create()
    except Exception, e:
        log.debug( "Creating slurm_account table failed: %s" % str( e ) )

    try:
        galaxy_user_slurm_account.create()
    except Exception, e:
        log.debug( "Creating galaxy_user_slurm_account table failed: %s" % str( e ) )


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()

    try:
        galaxy_user_slurm_account.drop()
    except Exception, e:
        log.debug( "Dropping galaxy_user_slurm_account table failed: %s" % str( e ) )

    try:
        slurm_account.drop()
    except Exception, e:
        log.debug( "Dropping slurm_account table failed: %s" % str( e ) )


