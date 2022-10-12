#!/usr/bin/env python
from abc import ABC

import rich_click as click
import multiprocessing
import uvicorn as unicorn  # lol
import celery

from gunicorn.app.base import BaseApplication
from typing import Any, Callable, Dict, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from asgiref.typing import ASGIApplication

from rich.traceback import install
install(show_locals=True)


def number_of_cpus():
    return multiprocessing.cpu_count()


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(BaseApplication, ABC):
    def __init__(self, application: Union["ASGIApplication", Callable, str],
                 options: Dict[str, Any] = None):
        self.options = options or {}
        self.application = application
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


@click.group()
def cli():
    pass


@cli.command()
@click.option('--module', default='app.asgi:app', help='Python module for uvicorn to run.', show_default=True)
@click.option('--host', default='0.0.0.0', help='Address to listen on.', show_default=True)
@click.option('--port', default=8080, help='Port to listen on.', show_default=True)
@click.option('--workers', default=1, help='Number of workers to use.', show_default=True)
@click.option('--log-level', default='info', help='Log level to use.', show_default=True)
def uvicorn(module: str, host: str, port: int, workers: int, log_level: str):
    unicorn.run(module, host=host, port=port, log_level=log_level.lower(), workers=workers)


@cli.command()
@click.option('--module', default='app.asgi:app', help='Python module for uvicorn to run.', show_default=True)
@click.option('--host', default='0.0.0.0', help='Address to listen on.', show_default=True)
@click.option('--port', default=8080, help='Port to listen on.', show_default=True)
@click.option('--workers', default=number_of_workers(), help='Number of workers to use.', show_default=True)
@click.option('--log-level', default='info', help='Log level to use.', show_default=True)
def gunicorn(module: str, host: str, port: int, workers: int, log_level: str):
    options = {
        "bind": "%s:%s" % (host, port),
        "workers": workers,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "loglevel": log_level
    }
    StandaloneApplication(module, options).run()


@cli.group(name="celery")
def celery_group():
    pass


@celery_group.command(name="worker")
@click.option('--app', '-A', default='app.tasks', help='Application', show_default=True)
@click.option('--broker', '-b', default='redis://localhost:6379/0', help='', show_default=True)
@click.option('--result-backend', default=None, help='', show_default=True)
@click.option('--task-events', '-E', is_flag=True, help='Enable sending task events.', show_default=True)
@click.option('--hostname', '-n', default="celery@%h", help='Set custom hostname.', show_default=True)
@click.option('--concurrency', '-c', default=number_of_cpus(), help='Number of concurrent processes/threads.',
              show_default=True)
@click.option('--log-level', default='info', help='Logging level.', show_default=True)
def worker_command(app: str, broker: str, result_backend: str, task_events: bool, hostname: str, concurrency: int,
                   log_level: str):
    a = celery.Celery()

    celery_args = ['--app', app, '--broker', broker]
    if result_backend is not None:
        celery_args.extend(['--result-backend', result_backend])

    worker_args = ['worker',
                   '--hostname', hostname,
                   '--concurrency', str(concurrency),
                   f'--loglevel={log_level.lower()}']
    if task_events:
        worker_args.append('--task-events')

    args = celery_args + worker_args
    print(args)

    a.start(argv=args)


@celery_group.command(name="beat")
@click.option('--app', '-A', default='app.tasks', help='Application', show_default=True)
@click.option('--log-level', default='info', help='Logging level.', show_default=True)
def beat_command(app: str, log_level: str):
    a = celery.Celery()
    celery_args = ['--app', app]
    beat_args = ['beat', f'--loglevel={log_level.lower()}']
    args = celery_args + beat_args
    a.start(argv=args)


@celery_group.command(name="flower")
@click.option('--app', '-A', default='app.tasks', help='Application', show_default=True)
@click.option('--broker', '-b', default='redis://localhost:6379/0', help='', show_default=True)
@click.option('--result-backend', default=None, help='', show_default=True)
@click.option('--address', '-a', default='0.0.0.0', help='Address to listen on.', show_default=True)
@click.option('--port', '-p', default=5555, help='Port to listen on.', show_default=True)
def flower_command(app: str, broker: str, result_backend: str, address: str, port: int):
    a = celery.Celery()

    celery_args = ['--app', app, '--broker', broker]
    if result_backend is not None:
        celery_args.extend(['--result-backend', result_backend])

    flower_args = ['flower', f'--address={address}', f'--port={port}']
    args = celery_args + flower_args
    a.start(argv=args)


if __name__ == '__main__':
    cli()
