#!/bin/bash
. .env
envsubst < config/prod_config.yml > config/config.yml

alembic revision --autogenerate -m "Init"
alembic upgrade head
python main.py
