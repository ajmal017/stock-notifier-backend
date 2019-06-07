#!/usr/bin/env bash      
set -e

export SERVER_PRIVATE_KEY=$(aws ssm get-parameters --names server.server_private_key --region us-west-1 --with-decryption --query Parameters[0].Value --output text)
export DB_USERNAME=$(aws ssm get-parameters --names server.db_username --region us-west-1 --with-decryption --query Parameters[0].Value --output text)
export DB_PASSWORD=$(aws ssm get-parameters --names server.db_password --region us-west-1 --with-decryption --query Parameters[0].Value --output text)

exec python /server/http_handler.py
