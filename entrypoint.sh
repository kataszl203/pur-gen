#!/bin/sh
gunicorn app:server -b 0.0.0.0:8080
