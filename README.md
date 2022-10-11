# asgi_falcon
This base image runs an ASGI Falcon application via Uvicorn.

[Docker Hub](https://hub.docker.com/r/nomb85/uvicorn_falcon)

### Uvicorn

Uvicorn will run with a default worker count of 1. The reason for this is if you are running uvicorn, you are probably 
not wanting to use a process manager and instead handle it at the cluster level.

To run uvicorn with defaults:
```bash
$ podman run -d -p 8080:8080 --name asgi_falcon nomb85/asgi_falcon:latest uvicorn
```

To run overriding uvicorn options:
```bash
$ podman run -d -p 8080:8080 --name asgi_falcon nomb85/asgi_falcon:latest uvicorn --host 0.0.0.0 --port 8080 --workers 4 --log-level info
```

To view uvicorn options:
```bash
$ podman run --rm --name asgi_falcon nomb85/asgi_falcon:latest uvicorn --help

 Usage: start.py uvicorn [OPTIONS]                                              
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --module       TEXT     Python module for uvicorn to run.                    │
│                         [default: app.asgi:app]                              │
│ --host         TEXT     Address to listen on. [default: 0.0.0.0]             │
│ --port         INTEGER  Port to listen on. [default: 8080]                   │
│ --workers      INTEGER  Number of workers to use. [default: 1]               │
│ --log-level    TEXT     Log level to use. [default: info]                    │
│ --help                  Show this message and exit.                          │
╰──────────────────────────────────────────────────────────────────────────────╯                                                                          
```

### Gunicorn

Gunicorn will run with a worker count that is automatically scaled based on your CPU count. 
If you want to override this, you can set the `--workers` option to a number of your choosing.

To run gunicorn with defaults:
```bash
$ podman run -d -p 8080:8080 --name asgi_falcon nomb85/asgi_falcon:latest gunicorn
```

To run overriding gunicorn options:
```bash
$ podman run -d -p 8080:8080 --name asgi_falcon nomb85/asgi_falcon:latest gunicorn --host 0.0.0.0 --port 8080 --workers 4 --log-level info
```

To view uvicorn options:
```bash
$ podman run --rm --name asgi_falcon nomb85/asgi_falcon:latest gunicorn --help

 Usage: start.py gunicorn [OPTIONS]                                             
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --module       TEXT     Python module for uvicorn to run.                    │
│                         [default: app.asgi:app]                              │
│ --host         TEXT     Address to listen on. [default: 0.0.0.0]             │
│ --port         INTEGER  Port to listen on. [default: 8080]                   │
│ --workers      INTEGER  Number of workers to use. [default: 41]              │
│ --log-level    TEXT     Log level to use. [default: info]                    │
│ --help                  Show this message and exit.                          │
╰──────────────────────────────────────────────────────────────────────────────╯
                                                                        
```

