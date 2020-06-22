"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count()


bind         = '127.0.0.1:' + environ.get('PORT', '8081')
max_requests = 1000
workers      = max_workers()