#!/usr/bin/env bash      
set -e

export ALPHA_VANTAGE_KEYS=$(aws ssm get-parameters --names server.alpha_vantage_keys --region us-west-1 --with-decryption --query Parameters[0].Value --output text)
export FIREBASE_API_KEY=$(aws ssm get-parameters --names server.firebase_api_key --region us-west-1 --with-decryption --query Parameters[0].Value --output text)

exec python /server/push_notifier.py "['AMD', 'LOVE', 'SLAB', 'AAPL', 'GOOG', 'SYMC', 'FB', 'TSLA', 'QCOM']"
