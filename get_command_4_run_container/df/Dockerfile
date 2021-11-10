FROM cucker/python:python_docker_1.0
LABEL maintainer='Image Maintainers <hanxiao2100@qq.com>'

COPY py/parse_container_inspect.py /

ENTRYPOINT [ "python", "/parse_container_inspect.py" ]
CMD [ "--help" ]
