#!/bin/bash
# Enable cron
service cron start

# Ensure env vars are passed to cron
printenv | grep -v "no_proxy" >> /etc/environment

echo "Starting Stock Web Service..."
python instock/web/web_service.py
