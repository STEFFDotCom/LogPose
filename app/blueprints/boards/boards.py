from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Board, UserTeam

boards = Blueprint("boards", __name__)

# main menu for boards - show all boards for the user
# GET is the only thing we need since we just need to serve the boards to the user
@boards.route("/boards", methods = ["GET"])
@login_required
def my_boards():

    # match current user ID to boards ID in the DB so we can return the users personal boards
    get_personal_boards_from_db = Board.query.filter_by(user_id = current_user.id).all()

    # return all rows where the current user ID matches in UserTeam
    team_ids_for_current_user = UserTeam.query.filter_by(user_id = current_user.id).all()

    # create a list with only the team_ids from the rows above
    team_ids = []
    for value in team_ids_for_current_user:
        team_ids.append(value.team_id)

    # here we match the IDs from team_ids list against the team id in Boards and also making sure the board is_shared
    get_shared_boards_from_db = Board.query.filter(Board.team_id.in_(team_ids), Board.is_shared == True).all()

    return render_template("boards/dashbaord.html", personal_boards = get_personal_boards_from_db, shared_boards = get_shared_boards_from_db)

# GET serve the create board page
# POST submit new board info to the DB and create it
@boards.route("/boards/create", methods = ["GET", "POST"])
@login_required
def create_board():
    pass

# GET we serve the board the user wants to view
@boards.route("/boards/<int:board_id>", methods = ["GET"])
@login_required
def view_board(board_id):
    pass

# POST the user click a button and confirm to delete button, we delete it in DB
@boards.route("/boards/<int:board_id>/delete", methods = ["POST"])
@login_required
def delete_board(board_id):
    pass