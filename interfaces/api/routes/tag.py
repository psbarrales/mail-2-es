from flask import Blueprint, jsonify, request
from app.services.tag import TagServices

tag = Blueprint("tag", __name__)


@tag.route("/tag", methods=["POST"])
def create_tag_controller():
    service = TagServices()
    response = service.create(request.json)
    return jsonify({"tag": response.dict()})


@tag.route("/tag", methods=["GET"])
def get_tags_controller():
    service = TagServices()
    tags = service.getAll()
    return jsonify([tag.dict() for tag in tags])
