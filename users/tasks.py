import requests
from TaskApp.celery import app
from .utils import Util


@app.task()
def write_file(email):
    Util.send_verification_email(email)
    return True