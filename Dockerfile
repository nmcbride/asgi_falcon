FROM python:3.10

WORKDIR /falcon_app

COPY ./requirements.txt /falcon_app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /falcon_app/requirements.txt

COPY ./start.py /falcon_app/start.py
COPY ./app /falcon_app/app

ENTRYPOINT ["python", "start.py"]
CMD ["uvicorn"]