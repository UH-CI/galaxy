#!/bin/bash

bash /home/galaxy/galaxy-dist/scripts/cleanup_datasets/delete_userless_histories.sh
bash /home/galaxy/galaxy-dist/scripts/cleanup_datasets/purge_histories.sh
bash /home/galaxy/galaxy-dist/scripts/cleanup_datasets/purge_libraries.sh
bash /home/galaxy/galaxy-dist/scripts/cleanup_datasets/purge_folders.sh
bash /home/galaxy/galaxy-dist/scripts/cleanup_datasets/purge_datasets.sh
