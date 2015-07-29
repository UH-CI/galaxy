#!/bin/bash

python scripts/manage_db.py version_control --repository=lib/third_party/slurm/database/migrate
python scripts/manage_db.py upgrade --repository=lib/third_party/slurm/database/migrate
