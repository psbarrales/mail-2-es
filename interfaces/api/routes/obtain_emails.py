from flask import Blueprint, jsonify
import datetime
from app.services.process_email import ProcessEmailService

obtain_emails = Blueprint("obtain_emails", __name__)
start_time = datetime.datetime.now()


@obtain_emails.route("/obtain_emails")
def obtain_emails_controller():
    service = ProcessEmailService()
    response = service.run()
    obtain_emails_info = {"mails": {"count": response}}
    return jsonify(obtain_emails_info)
