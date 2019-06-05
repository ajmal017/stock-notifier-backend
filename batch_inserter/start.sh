#!/usr/bin/env bash      
set -e

export ALPHA_VANTAGE_KEYS=$(aws ssm get-parameters --names server.alpha_vantage_keys --region us-west-1 --with-decryption --query Parameters[0].Value --output text)

exec python /server/database_adder.py
