#!/bin/bash
. .env
envsubst < config/prod_config.yml > config/config.yml

alembic upgrade head
python main.py
