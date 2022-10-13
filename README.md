# asgi_falcon
This base image runs an ASGI Falcon application via Uvicorn or Gunicorn.

[Docker Hub](https://hub.docker.com/r/nomb85/asgi_falcon/tags)

```bash
podman pull docker.io/nomb85/asgi_falcon
```

## Uvicorn

Uvicorn will run with a default worker count of 1. The reason for this is if you are running uvicorn, you are probably 
not wanting to use a process manager and instead handle it at the cluster level.

To run uvicorn:
```bash
$ podman run -d -p 8080:8080 --name asgi_falcon nomb85/asgi_falcon:latest
```
or
```bash
$ podman run -d -p 8080:8080 --name asgi_falcon nomb85/asgi_falcon:latest uvicorn
```

```bash
$ podman run --rm --name asgi_falcon nomb85/asgi_falcon:latest uvicorn --help

Usage: start.py uvicorn [OPTIONS]

Options:
  --module TEXT      Python module for uvicorn to run.  [default:
                     app.asgi:app]
  --host TEXT        Address to listen on.  [default: 0.0.0.0]
  --port INTEGER     Port to listen on.  [default: 8080]
  --workers INTEGER  Number of workers to use.  [default: 1]
  --log-level TEXT   Log level to use.  [default: info]
  --help             Show this message and exit.                                                                        
```

## Gunicorn

Gunicorn will run with a worker count that is automatically scaled based on your CPU count. 
If you want to override this, you can set the `--workers` option to a number of your choosing.

To run gunicorn:
```bash
$ podman run -d -p 8080:8080 --name asgi_falcon nomb85/asgi_falcon:latest gunicorn
```

```bash
$ podman run --rm --name asgi_falcon nomb85/asgi_falcon:latest gunicorn --help

Usage: start.py gunicorn [OPTIONS]

Options:
  --module TEXT      Python module for uvicorn to run.  [default:
                     app.asgi:app]
  --host TEXT        Address to listen on.  [default: 0.0.0.0]
  --port INTEGER     Port to listen on.  [default: 8080]
  --workers INTEGER  Number of workers to use.  [default: 41]
  --log-level TEXT   Log level to use.  [default: info]
  --help             Show this message and exit.                                                                        
```
## Celery

Along with the application, uvicorn and gunicorn, this image also contains celery and flower.

### worker

To run a worker:
```bash
$ podman run -d --name asgi_falcon nomb85/asgi_falcon:latest celery worker
```

```bash
Usage: start.py celery worker [OPTIONS]

Options:
  -A, --app TEXT             Application  [default: app.tasks]
  -b, --broker TEXT          [default: redis://localhost:6379/0]
  --result-backend TEXT
  -E, --task-events          Enable sending task events.
  -n, --hostname TEXT        Set custom hostname.  [default: celery@%h]
  -c, --concurrency INTEGER  Number of concurrent processes/threads.
                             [default: 20]
  --log-level TEXT           Logging level.  [default: info]
  --help                     Show this message and exit.
```

### beat

To run beat:

```bash
$ podman run -d --name asgi_falcon nomb85/asgi_falcon:latest celery beat
```

```bash
Usage: start.py celery beat [OPTIONS]

Options:
  -A, --app TEXT    Application  [default: app.tasks]
  --log-level TEXT  Logging level.  [default: info]
  --help            Show this message and exit.
```

### flower

To run flower:
```bash
$ podman run -d -p 5555:5555 --name asgi_falcon nomb85/asgi_falcon:latest flower
```

```bash
Usage: start.py celery flower [OPTIONS]

Options:
  -A, --app TEXT         Application  [default: app.tasks]
  -b, --broker TEXT      [default: redis://localhost:6379/0]
  --result-backend TEXT
  -a, --address TEXT     Address to listen on.  [default: 0.0.0.0]
  -p, --port INTEGER     Port to listen on.  [default: 5555]
  --help                 Show this message and exit.
```

### command

Due to the complexity of celery, there is an added command that allows you to run celery with any passed commands or arguments. Valid or not.

```bash
$ podman run --rm nomb85/asgi_falcon:beta celery command --args '["--version"]'
```

```bash

```

```bash
Usage: start.py celery command [OPTIONS]

Options:
  --args TEXT  Run a custom command.  [default: ["--version"]]
  --help       Show this message and exit.
```