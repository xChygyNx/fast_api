#!/bin/bash
sleep 10
python /src/python_bin/create_table.py
python /src/python_bin/create_cron_job.py
python /src/python_bin/container_reanimator.py
