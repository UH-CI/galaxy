"""
Utility helpers related to the model
"""

# TODO: Need to figure out how to access the database in a non-raw manner
def getSlurmAccount( sa_session, usrid):
    sql = """SELECT A.id, A.name, B.selected FROM slurm_account AS A JOIN galaxy_user_slurm_account AS B ON ( A.id = B.account_id) WHERE B.user_id = :usrid;"""
    return sa_session.execute(sql, {'usrid': usrid})


def getSlurmPartition( sa_session, usrid):
    sql = """SELECT A.id, A.name, B.selected FROM slurm_partition AS A JOIN galaxy_user_slurm_partition AS B ON ( A.id = B.partition_id) WHERE B.user_id = :usrid;"""
    return sa_session.execute(sql, {'usrid': usrid})


def getSlurmAccountPartition(sa_session, usrid):
    params = dict(usrid = usrid, sel = True)
    sql = """SELECT B.name FROM galaxy_user_slurm_account AS A JOIN slurm_account AS B ON (A.account_id = B.id)  WHERE user_id = :usrid AND selected = :sel; """
    sel_accnt = sa_session.execute(sql, params).fetchone()
    if sel_accnt:
        sel_accnt = sel_accnt[0]
    sql = """SELECT B.name, B.max_cpus, B.max_time, B.ram_per_cpu FROM galaxy_user_slurm_partition AS A JOIN slurm_partition AS B ON (A.partition_id = B.id) WHERE A.user_id = :usrid AND A.selected = :sel; """
    part_row = sa_session.execute(sql, params).fetchone()
    if part_row:
        partition, max_cpus, max_time, ram_per_cpu = part_row
    else:
        partition, max_cpus, max_time, ram_per_cpu = (None, None, None, None,)
    return sel_accnt, partition, max_cpus, max_time, ram_per_cpu


def getSlurmAccountPartitionCombos(sa_session, usrid):
    params = dict(usrid = usrid, sel = True)
    sql = """SELECT account_id FROM galaxy_user_slurm_account WHERE user_id = :usrid AND selected = :sel; """
    sel_accnt = sa_session.execute(sql, params).fetchone()
    if sel_accnt:
        sel_accnt = sel_accnt[0]

    sql = """SELECT partition_id, max_cpus, max_time, ram_per_cpu FROM galaxy_user_slurm_partition WHERE user_id = :usrid AND selected = :sel; """
    sel_part = sa_session.execute(sql, params).fetchone()
    if sel_part:
        sel_part = sel_part[0]

    sql = """SELECT account, partition, account_id, partition_id
              FROM 
               (SELECT B.id AS accntid, C.id AS partid, B.name AS account, C.name AS partition 
               FROM slurm_partition_to_account AS A 
               JOIN slurm_account AS B ON (A.account_id = B.id) 
               JOIN slurm_partition AS C ON (A.partition_id = C.id)) AS D 
               JOIN galaxy_user_slurm_account AS E ON (D.accntid = E.account_id) 
               JOIN galaxy_user_slurm_partition AS F ON (F.partition_id = D.partid) 
              WHERE E.user_id = :usrid AND F.user_id = :usrid;"""
    return (sa_session.execute(sql, {'usrid': usrid}), sel_accnt, sel_part, )


def setSlurmAccount(sa_session, usrid, accountlabel):
    param_false = dict(usrid = usrid, sel = False)
    if accountlabel == 'DEFAULT':
        sql = """UPDATE galaxy_user_slurm_account SET selected = :sel WHERE user_id = :usrid;"""
        sa_session.execute(sql, param_false)
    else:
        sql = """SELECT id FROM slurm_account WHERE name = :lbl;"""
        result = sa_session.execute(sql, {'lbl': accountlabel})
        accountid = result.fetchone()[0]
        result.close()
        param_true = dict(usrid = usrid, sel = True, accnt = accoutid)
        sql = """UPDATE galaxy_user_slurm_account SET selected = :sel WHERE user_id = :usrid;"""
        sa_session.execute(sql, param_false)
        sql = """UPDATE galaxy_user_slurm_account SET selected = :sel WHERE user_id = :usrid AND account_id = :accnt;"""
        sa_session.execute(sql, param_true)


def setSlurmPartition(sa_session, usrid, partition):
    param_false = dict(usrid = usrid, sel = False)
    if partition == 'DEFAULT':
        sql = """UPDATE galaxy_user_slurm_partition SET selected = :sel WHERE user_id = :usrid;"""
        sa_session.execute(sql, param_false)
    else:
        sql = """SELECT id FROM slurm_partition WHERE name = :lbl;"""
        result = sa_session.execute(sql, {'lbl': partition})
        accountid = result.fetchone()[0]
        result.close()
        param_true = dict(usrid = usrid, sel = True, accnt = accoutid)
        sql = """UPDATE galaxy_user_slurm_partition SET selected = :sel WHERE user_id = :usrid;"""
        sa_session.execute(sql, param_false)
        sql = """UPDATE galaxy_user_slurm_partition SET selected = :sel WHERE user_id = :usrid AND partition_id = :accnt;"""
        sa_session.execute(sql, param_true)


def setSlurmAccountandPartition(sa_session, usrid, account_partition):
    
    setSlurmAccount(sa_session, usrid, account_partition['account'])
    setSlurmPartition(sa_session, usrid, account_partition['partition'])


# model.slurm_account = Table( "slurm_account", metadata,
#     Column( "id", Integer, primary_key=True ),
#     Column( "name", TEXT, default = False  ) )

# model.galaxy_user_slurm_account = Table( "galaxy_user_slurm_account", metadata,
#     Column( "id", Integer, primary_key = True ),
#     Column( "account_id", Integer, ForeignKey("slurm_account.id"), index = True),
#     Column( "user_id", Integer, ForeignKey( "galaxy_user.id" ), index = True ),
#     Column( "selected", Boolean, default = False, index = True  ) )

# model.slurm_partition = Table( "slurm_partition", metadata,
#     Column( "id", Integer, primary_key=True ),
#     Column( "name", TEXT, default = False  ) )

# model.galaxy_user_slurm_partition = Table( "galaxy_user_slurm_partition", metadata,
#     Column( "id", Integer, primary_key = True ),
#     Column( "partition_id", Integer, ForeignKey("slurm_partition.id"), index = True),
#     Column( "user_id", Integer, ForeignKey( "galaxy_user.id" ), index = True ),
#     Column( "selected", Boolean, default = False, index = True  ) )

# model.slurm_partition_to_account = Table( "slurm_partition_to_account", metadata,
#     Column( "id", Integer, primary_key = True ),
#     Column( "account_id", Integer, ForeignKey("slurm_account.id"), index = True),
#     Column( "partition_id", Integer, ForeignKey( "slurm_partition.id" ), index = True ) )
