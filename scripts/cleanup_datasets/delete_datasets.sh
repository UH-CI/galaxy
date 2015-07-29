#!/bin/sh

cd `dirname $0`/../..
python ./scripts/cleanup_datasets/cleanup_datasets.py ./config/galaxy.ini -d 30 -6 -r $@ >> ./scripts/cleanup_datasets/delete_datasets.log
