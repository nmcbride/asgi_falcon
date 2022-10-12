from celery import *


app = Celery('asgi_falcon')
app.config_from_object('app.celeryconfig')


@app.task
def add(x, y):
    return x + y


if __name__ == '__main__':
    app.start()
