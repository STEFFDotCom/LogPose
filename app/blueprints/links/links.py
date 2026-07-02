from flask import Blueprint
from flask_login import login_required
from app import db

links = Blueprint("links", __name__)

@links.route("/boards/<int:board_id>/links/create", methods = ["POST"])
@login_required
def create_link(board_id):
    pass

@links.route("/links/<int:link_id>/delete", methods = ["POST"])
@login_required
def delete_link(link_id):
    pass

@links.route("/links/<int:link_id>/edit", methods = ["POST"])
@login_required
def edit_link(link_id):
    pass