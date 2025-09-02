#!/usr/bin/env bash
python3 -m venv venv
source venv/bin/activate
pip install gunicorn
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:$PORT app:app