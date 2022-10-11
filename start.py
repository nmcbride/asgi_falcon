#!/usr/bin/env python

import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--module', default='app.asgi:app', help='Python module for uvicorn to run.')
@click.option('--host', default='0.0.0.0', help='IP Address to listen on.')
@click.option('--port', default=8080, help='Port to listen on.')
@click.option('--log-level', default='info', help='Log level to use.')
def uvicorn(module, host, port, log_level):
    import uvicorn
    log_level = log_level.lower()
    uvicorn.run(module, host=host, port=port, log_level=log_level)


if __name__ == '__main__':
    cli()
