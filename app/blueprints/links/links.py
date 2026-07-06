from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Board, UserTeam, Group

links = Blueprint("links", __name__)

@links.route("/boards/<int:board_id>/links/create", methods = ["POST"])
@login_required
def create_link(board_id):
    
    # get row of pressed board
    get_board_row = Board.query.filter_by(id = board_id).first()
    


    pass

@links.route("/links/<int:link_id>/delete", methods = ["POST"])
@login_required
def delete_link(link_id):
    pass

@links.route("/links/<int:link_id>/edit", methods = ["POST"])
@login_required
def edit_link(link_id):
    pass