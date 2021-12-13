FROM cucker/python:python_docker_1.1
LABEL maintainer='Image Maintainers <hanxiao2100@qq.com>'

COPY py/parse_stack.py /

ENTRYPOINT [ "python", "/parse_stack.py" ]
CMD [ "--help" ]
