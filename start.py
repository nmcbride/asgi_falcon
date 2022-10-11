#!/usr/bin/env python
from abc import ABC

import rich_click as click
import multiprocessing
import uvicorn as unicorn  # lol

from gunicorn.app.base import BaseApplication
from typing import Any, Callable, Dict, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from asgiref.typing import ASGIApplication

from rich.traceback import install
install(show_locals=True)


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


if __name__ == '__main__':
    cli()
