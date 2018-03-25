#!/bin/bash
#A sample Bash script, by Michael
./setup.txt
 pip install --upgrade sqlalchemy==1.2.0b3
./db_create.py
./db_migrate.py
