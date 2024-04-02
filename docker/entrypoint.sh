#!/bin/sh

set -e

# Iniciar el servicio cron
cron

# Prepare database
alembic upgrade head

# Ejecutar la aplicación Flask
python __main__.py --server