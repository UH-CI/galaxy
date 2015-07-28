"""
Migration script to create tables to manage mapping users to partitions, as well as partitions to accounts
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

slurm_partition = Table( "slurm_partition", metadata,
                         Column( "id", Integer, primary_key=True ),
                         Column( "name", TEXT, default = False  ),
                         Column( "max_time", TEXT),
                         Column( "max_cpus", Integer),
                         Column( "ram_per_cpu", Integer),
 )


galaxy_user_slurm_partition = Table( "galaxy_user_slurm_partition", metadata,
    Column( "id", Integer, primary_key=True ),
    Column( "partition_id", Integer, ForeignKey("slurm_partition.id"), index=True),
    Column( "user_id", Integer, ForeignKey( "galaxy_user.id" ), index=True ),
    Column( "selected", Boolean, default = False, index = True  ) )
#    Column( "default", Boolean, default = False, index = True  ) )

slurm_partition_to_account = Table( "slurm_partition_to_account", metadata,
    Column( "id", Integer, primary_key=True ),
    Column( "account_id", Integer, ForeignKey("slurm_account.id"), index=True),
    Column( "partition_id", Integer, ForeignKey( "slurm_partition.id" ), index=True ) )
#    Column( "default", Boolean, default = False, index = True  ) )


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    print __doc__
    metadata.reflect()

    try:
        slurm_partition.create()
    except Exception, e:
        log.debug( "Creating slurm_partition table failed: %s" % str( e ) )

    try:
        slurm_partition_to_account.create()
    except Exception, e:
        log.debug( "Creating slurm_partition_to_account table failed: %s" % str( e ) )

    try:
        galaxy_user_slurm_partition.create()
    except Exception, e:
        log.debug( "Creating galaxy_user_slurm_partition table failed: %s" % str( e ) )


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()
    try:
        galaxy_user_slurm_partition.drop()
    except Exception, e:
        log.debug( "Dropping galaxy_user_slurm_partition table failed: %s" % str( e ) )

    try:
         slurm_partition_to_account.drop()
    except Exception, e:
        log.debug( "Dropping slurm_partition_to_account table failed: %s" % str( e ) )

    try:
         slurm_partition.drop()
    except Exception, e:
        log.debug( "Dropping slurm_partition table failed: %s" % str( e ) )


