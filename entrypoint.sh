#!/bin/sh
gunicorn --timeout 4800 app:server -b 0.0.0.0:8080