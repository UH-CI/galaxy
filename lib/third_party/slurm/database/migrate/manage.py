#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='sqlite:///./database/universe.sqlite?isolation_level=IMMEDIATE', debug='False')
