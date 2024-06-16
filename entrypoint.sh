#!/bin/sh
gunicorn --timeout 2400 app:server -b 0.0.0.0:8080