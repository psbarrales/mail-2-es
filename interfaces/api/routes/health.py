from flask import Blueprint, jsonify
import datetime

health = Blueprint("health", __name__)
start_time = datetime.datetime.now()


@health.route("/health")
def health_controller():
    health_info = {
        "status": "ok",
        "version": "1.0.0",
        "uptime": str(
            datetime.datetime.now() - start_time
        ),  # Suponiendo que `start_time` es cuando la app inició
        "timestamp": datetime.datetime.now().isoformat(),
    }
    return jsonify(health_info)
