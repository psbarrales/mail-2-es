from flask import Flask
from .routes import routes

app = Flask(__name__)
routes(app)
