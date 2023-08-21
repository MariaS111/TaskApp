from TaskApp.celery import app
from .utils import Util


@app.task()
def send_verify_email(email):
    Util.send_verification_email(email)
    return True


@app.task()
def send_marketing_email():
    Util.send_email()
    return True
