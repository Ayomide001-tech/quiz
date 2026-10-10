#!/usr/bin/env bash
# Exit on error

        
set -o errexit
pip install -r quiz/requirements.txt
python quiz/manage.py collectstatic --no-input
python quiz/manage.py migrate