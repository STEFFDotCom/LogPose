from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Board, UserTeam, Team

boards = Blueprint("boards", __name__)

# main menu for boards - show all boards for the user
# GET is the only thing we need since we just need to serve the boards to the user
@boards.route("/boards", methods = ["GET"])
@login_required
def my_boards():

    # match current user ID to boards ID in the DB so we can return the users personal boards
    get_personal_boards_from_db = Board.query.filter_by(user_id = current_user.id).all()

    # return all rows where the current user ID matches in UserTeam table
    team_ids_for_current_user = UserTeam.query.filter_by(user_id = current_user.id).all()

    # create a list with only the team_ids from the rows above
    team_ids = []
    for value in team_ids_for_current_user:
        team_ids.append(value.team_id)

    # here we match the IDs from team_ids list against the team id in Boards and also making sure the board is_shared
    get_shared_boards_from_db = Board.query.filter(Board.team_id.in_(team_ids), Board.is_shared == True).all()

    return render_template("boards/dashboard.html", personal_boards = get_personal_boards_from_db, shared_boards = get_shared_boards_from_db)

# GET serve the create board page
# POST submit new board info to the DB and create it
@boards.route("/boards/create", methods = ["GET", "POST"])
@login_required
def create_board():
    
    if request.method == "GET":
        
        # return all rows where the current user id matches in UserTean table
        team_ids_for_current_user = UserTeam.query.filter_by(user_id = current_user.id).all()

        # get UserTeam ids
        team_ids = []

        for team_id in team_ids_for_current_user:
            team_ids.append(team_id.team_id)
        
        # hold the ids up against the team table and return all rows that match
        team_rows = Team.query.filter(Team.id.in_(team_ids)).all()

        return render_template("boards/create_board.html", teams = team_rows)
    
    if request.method == "POST":
        
        new_board_name = request.form.get("input_board_name")

        # get either personal or shared
        personal_or_shared = request.form.get("board_type")

        selected_team_id = request.form.get("selected_team")

        # get the row where user and teamid match, so we can get the role
        if selected_team_id:
            check_user_role = UserTeam.query.filter_by(user_id = current_user.id, team_id = selected_team_id).first()
            
            if check_user_role:
                if check_user_role.role == "editor":
                    # create new board with info from user
                    new_shared_board = Board(board_name = new_board_name, is_shared = True, team_id = selected_team_id)
                    # add it to the DB
                    db.session.add(new_shared_board)
                    # commit it to the DB(SAVE IT)
                    db.session.commit()
                    flash("Board created successfully", "success")
                    return redirect(url_for("boards.my_boards"))
                elif check_user_role.role == "viewer":
                    flash("You do not have permission to create a board for this team", "danger")
                    return redirect(url_for("boards.create_board"))
            else:
                flash("Your missing permission or are not a member of this team. Please contact admin", "danger")
                return redirect(url_for("boards.create_board"))

        if personal_or_shared == "personal":
            new_personal_board = Board(board_name = new_board_name, is_shared = False, user_id = current_user.id)
            db.session.add(new_personal_board)
            db.session.commit()
            flash("Personal board successfully created", "success")
            return redirect(url_for("boards.my_boards"))

# GET we serve the board the user wants to view
@boards.route("/boards/<int:board_id>", methods = ["GET"])
@login_required
def view_board(board_id):
    
    # get the row of the board pressed
    get_board_row = Board.query.filter_by(id = board_id).first()

    # permission checks for clicked board
    if get_board_row:
        if get_board_row.is_shared == False:
            if get_board_row.user_id == current_user.id:
                return render_template("boards/view_board.html", board_info = get_board_row)
            else:
                flash("You do not have permission to view this - contact admin", "danger")
                return redirect(url_for("boards.my_boards"))
        elif get_board_row.is_shared == True:
            check_team = UserTeam.query.filter_by(team_id = get_board_row.team_id, user_id = current_user.id).first()
            if check_team:
                return render_template("boards/view_board.html", board_info = get_board_row)
            else:
                flash("You do not have permission to view this - contact admin", "danger")
                return redirect(url_for("boards.my_boards"))
    else:
        flash("Board does not exist or an error happened - contact admin", "danger")
        return redirect(url_for("boards.my_boards"))

# POST the user click a button and confirm to delete button, we delete it in DB
@boards.route("/boards/<int:board_id>/delete", methods = ["POST"])
@login_required
def delete_board(board_id):
    pass