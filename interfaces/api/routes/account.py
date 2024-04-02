from flask import Blueprint, jsonify, request
from app.services.account import AccountServices

account = Blueprint("account", __name__)


@account.route("/account", methods=["POST"])
def create_account_controller():
    service = AccountServices()
    response = service.create(request.json)
    return jsonify({"account": response.dict()})


@account.route("/account", methods=["GET"])
def get_accounts_controller():
    service = AccountServices()
    accounts = service.getAll()
    return jsonify([account.dict() for account in accounts])
