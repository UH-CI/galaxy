from galaxy.jobs import JobDestination
import os
from third_party.slurm.database.util import getSlurmAccountPartition

"""
    <destination id="slurm_dynamic" runner="dynamic">
      <param id="type">python</param>
      <param id="function">slurm_dynamic_wrapper</param>
    </destination>
"""

def slurm_dynamic_wrapper(app, user):
    usrid = user.id
    account, partition, max_cpus, max_time, ram_per_cpu = getSlurmAccountPartition(app.model.context, usrid)

    native_specs = """-p community.q -N 1 -n 20 --mem=102500 -t 72:00"""

    if partition:
        native_specs = """-p %(partition) -N 1 -n %(max_cpus) --mem=%(max_mem) -t %(max_time)"""%dict(partition=partition, max_cpus=max_cpus, max_mem = int(max_cpus) * int(ram_per_cpu), max_time = max_time)
    if account:
        native_specs = """-A %(account) %(nspec)"""%dict(accont=account, nspec = native_specs)

    params = dict(submit_native_specification = native_specs, 
                  default_file_action = "none", 
                  submit_user = user.username, 
                  file_action_config = "/lus/scratch/galaxy/config/galaxy/file_action.yml", 
                  private_token="", 
                  url = "")

    return JobDestination(runner="pulsar", params=params)
