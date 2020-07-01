FROM python:3.8.3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
COPY requirements-dev.txt /code/
RUN pip install -r requirements-dev.txt --quiet
COPY . /code/
