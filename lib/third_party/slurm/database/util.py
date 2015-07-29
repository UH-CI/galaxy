"""
Utility helpers related to the model
"""

# TODO: Need to figure out how to access the database in a non-raw manner
def getSlurmAccount( sa_session, id):
    sql = """SELECT A.id, A.name, B.selected FROM slurm_account AS A JOIN galaxy_user_slurm_account AS B ON ( A.id = B.account_id) WHERE B.user_id = :id;"""
    return sa_session.execute(sql, {'id': id})

# model.slurm_account = Table( "slurm_account", metadata,
#     Column( "id", Integer, primary_key=True ),
#     Column( "name", TEXT, default = False  ) )

# model.galaxy_user_slurm_account = Table( "galaxy_user_slurm_account", metadata,
#     Column( "id", Integer, primary_key=True ),
#     Column( "account_id", Integer, ForeignKey("slurm_account.id"), index=True),
#     Column( "user_id", Integer, ForeignKey( "galaxy_user.id" ), index=True ),
#     Column( "selected", Boolean, default = False  ) )


# model.slurm_partition = Table( "slurm_partition", metadata,
#     Column( "id", Integer, primary_key=True ),
#     Column( "name", TEXT, default = False  ) )

# model.galaxy_user_slurm_partition = Table( "galaxy_user_slurm_partition", metadata,
#     Column( "id", Integer, primary_key=True ),
#     Column( "partition_id", Integer, ForeignKey("slurm_partition.id"), index=True),
#     Column( "user_id", Integer, ForeignKey( "galaxy_user.id" ), index=True ),
#     Column( "selected", Boolean, default = False  ) )

# model.slurm_partition_to_account = Table( "slurm_partition_to_account", metadata,
#     Column( "id", Integer, primary_key=True ),
#     Column( "account_id", Integer, ForeignKey("slurm_account.id"), index=True),
#     Column( "partition_id", Integer, ForeignKey( "slurm_partition.id" ), index=True ) )
