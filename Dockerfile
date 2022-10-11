FROM python:3.10

WORKDIR /falcon_app

COPY ./requirements.txt /falcon_app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /falcon_app/requirements.txt

COPY ./app /falcon_app/app

CMD ["uvicorn", "app.asgi:app", "--host", "0.0.0.0", "--port", "80"]