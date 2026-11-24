#!/bin/bash
# Hosts service1 with Graftcode Gateway (gg) instead of consuming a RabbitMQ queue.
# Needs gg (https://github.com/grft-dev/graftcode-gateway/releases) and a Python with this
# service's dependencies installed. If gg cannot find libpython, set
# HYPERTUBE_PYTHON_RUNTIME_PATH=/path/to/libpython3.x.so (and PYTHONPATH to your site-packages).
cd "$(dirname "$0")"
exec gg --runtime python --modules ./graft/ --port "${GG_PORT:-8101}" --httpPort "${GG_HTTP_PORT:-8111}"
