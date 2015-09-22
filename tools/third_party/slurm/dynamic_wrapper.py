from galaxy.jobs import JobDestination
import os
from lockfile import LockFile # pip install lockfile
import yaml
from third_party.slurm.database.util import getSlurmAccountPartition

"""
    <destination id="slurm_dynamic" runner="dynamic">
      <param id="type">python</param>
      <param id="function">slurm_dynamic_wrapper</param>
    </destination>
"""

def slurm_dynamic_wrapper(app, user, tool_id):
    usrid = user.id
    account, partition, max_cpus, max_time, ram_per_cpu = getSlurmAccountPartition(app.model.context, usrid)

    native_specs = """-p community.q -N 1 -n 20 --mem=102500 -t 72:00"""


    lock = LockFile("dyn.lock")
    threadfile = "tool_threads.yml"
    with lock:
        tool_thrds = yaml.load(open(threadfile))
	if not tool_thrds:
	    tool_thrds = {}
        if tool_id in tool_thrds:
            thrds = int(tool_thrds.get(tool_id, 0))
            if thrds != 0:
                max_cpus = min(thrds, max_cpus)
                native_specs = """-p community.q -N 1 -n %s --mem=%s -t 72:00"""%(max_cpus, 102500 / max_cpus)
    
        else:
            tool_thrds[tool_id] = 0
            with open(threadfile, "w") as yml:
                yaml.dump(tool_thrds, yml)

    if partition:
        native_specs = """-p %(partition)s -N 1 -n %(max_cpus)s --mem=%(max_mem)s -t %(max_time)s"""%dict(partition=partition, max_cpus=max_cpus, max_mem = int(max_cpus) * int(ram_per_cpu), max_time = max_time)

    if account:
        native_specs = """-A %(account)s %(nspec)s"""%dict(account=account, nspec = native_specs)

    params = dict(submit_native_specification = native_specs, 
                  default_file_action = "none", 
                  submit_user = user.username, 
                  file_action_config = "", 
                  private_token="",
                  url = "")

    return JobDestination(runner="pulsar", params=params)
