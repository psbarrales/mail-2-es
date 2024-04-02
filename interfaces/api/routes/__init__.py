from flask import Flask
from .health import health
from .obtain_emails import obtain_emails
from .account import account
from .tag import tag


def routes(app: Flask):
    app.register_blueprint(health)
    app.register_blueprint(obtain_emails)
    app.register_blueprint(account)
    app.register_blueprint(tag)
