#!/bin/bash
. .env
envsubst < config/prod_config.yml > config/config.yaml

alembic revision --autogenerate -m "Init"
alembic upgrade head
python main.py
