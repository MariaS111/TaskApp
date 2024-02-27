FROM python:3.10
ENV PYTHONUNBUFFERED 1
COPY . /usr/src/taskapi
RUN pip install -r /usr/src/taskapi/requirements.txt
ENTRYPOINT ["/usr/src/taskapi/entrypoint.sh"]