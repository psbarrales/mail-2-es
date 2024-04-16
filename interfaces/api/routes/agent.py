from flask import Blueprint, jsonify, request
from app.services.agent import AgentServices

agent = Blueprint("agent", __name__)


@agent.route("/agent", methods=["POST"])
def create_account_controller():
    service = AgentServices()
    response = service.chat(request.json["message"])
    return jsonify({"response": response.dict()})
