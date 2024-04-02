from interfaces.api.server import app
import argparse
import logging
from dotenv import load_dotenv

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

# Condition to start the server only if the --server argument is passed
if args.server:
    app.run(host="::", port=8080, debug=True)
