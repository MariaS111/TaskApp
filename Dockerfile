FROM python:3.10
ENV PYTHONUNBUFFERED 1
COPY . /usr/src/taskapi
WORKDIR /usr/src/taskapi
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh
CMD ./entrypoint.sh
EXPOSE 8000