from interfaces.api.server import app
from interfaces.bot.bot import bot

import argparse
import logging
from dotenv import load_dotenv
import threading

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

parser = argparse.ArgumentParser(description="Starts the Flask application.")
parser.add_argument(
    "--server",
    action="store_true",
    help="Starts the Flask server if this argument is passed.",
)
args = parser.parse_args()


def run_server():
    app.run(host="::", port=8080, debug=True, use_reloader=False)


if args.server:
    flask_thread = threading.Thread(target=run_server)
    flask_thread.start()
    bot()
