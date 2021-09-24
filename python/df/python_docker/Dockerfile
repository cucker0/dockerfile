FROM python:3.9.6-alpine3.14
LABEL maintainer='Python with Docker module Maintainers <hanxiao2100@qq.com>'

COPY requirements.txt /usr/local/src/
RUN pip install --no-cache-dir -r /usr/local/src/requirements.txt
