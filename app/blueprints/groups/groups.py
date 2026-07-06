from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Board, UserTeam, Group
from sqlalchemy import func, select

groups = Blueprint("groups", __name__)

@groups.route("/boards/<int:board_id>/groups/create", methods = ["POST"])
@login_required
def create_group(board_id):

    # get row of pressed board
    get_board_row = Board.query.filter_by(id = board_id).first()
        
    # permission check
    if not get_board_row:
        flash("Board does not exist or an error happened - contact admin", "danger")
        return redirect(url_for("boards.my_boards"))
    elif get_board_row.is_shared == False:
        if get_board_row.user_id != current_user.id:
            flash("You do not have permission to view this - contact admin", "danger")
            return redirect(url_for("boards.my_boards"))
    elif get_board_row.is_shared == True:
        check_team = UserTeam.query.filter_by(team_id = get_board_row.team_id, user_id = current_user.id).first()
        if not check_team:
            flash("You do not have permission to view this - contact admin", "danger")
            return redirect(url_for("boards.my_boards"))
    
    # create the group
    new_group_name = request.form.get("GROUP_NAME_PLACEHOLDER")
    new_group_color = request.form.get("GROUP_COLOR_PLACEHOLDER")
    new_group_board_id = get_board_row.id
    query_max_position = select(func.max(Group.position)).where(Group.board_id == board_id)
    max_position = db.session.scalar(query_max_position)
    new_group = Group(group_name = new_group_name, group_color = new_group_color, board_id = new_group_board_id, position = (max_position + 1) if max_position is not None else 1)
    db.session.add(new_group)
    db.session.commit()
    flash("Group has been created!", "success")
    return redirect(url_for("boards.view_board", board_id = board_id))

@groups.route("/groups/<int:group_id>/delete", methods = ["POST"])
@login_required
def delete_group(group_id):

    # get row of pressed group
    get_group_row = Group.query.filter_by(id = group_id).first()

    # check if group exists and fetch the board id
    if get_group_row:
        board_id = get_group_row.board_id
    else:
        flash("Group does not exist", "danger")
        return redirect(url_for("boards.my_boards"))

    # get the entire board row
    get_board_row = Board.query.filter_by(id = board_id).first()
    
    # DEFENSIVE GUARD
    # make sure board exists, if board is shared that user is have editor role and if personal board that it is the correct user - then delete board
    if not get_board_row:
        flash("Board does not exist or an error happened - contact admin", "danger")
        return redirect(url_for("boards.my_boards"))
    elif get_board_row.is_shared == True:
        get_userteam_row = UserTeam.query.filter_by(user_id = current_user.id, team_id = get_board_row.team_id).first()
        if get_userteam_row.role != "editor":
            flash("You do not have permission to delete this group. If you want to have it deleted, contact admin.", "danger")
            return redirect(url_for("boards.view_board", board_id = board_id))
    elif get_board_row.is_shared == False:
        if get_board_row.user_id != current_user.id:
            flash("You do not have permission to delete this group. If you want to have it deleted, contact admin.", "danger")
            return redirect(url_for("boards.view_board", board_id = board_id))
    
    # delete the group
    db.session.delete(get_group_row)
    db.session.commit()
    flash("Group has been successfully deleted!", "success")
    return redirect(url_for("boards.view_board", board_id = board_id))


@groups.route("/groups/<int:group_id>/edit", methods = ["POST"])
@login_required
def edit_group(group_id):

    # get row of pressed group
    get_group_row = Group.query.filter_by(id = group_id).first()

    # make sure the group exists
    if get_group_row:
        board_id = get_group_row.board_id
    else:
        flash("Group does not exist", "danger")
        return redirect(url_for("boards.my_boards"))
    
    get_board_row = Board.query.filter_by(id = board_id).first()

    # permission check / defensive guard
    if not get_board_row:
        flash("Board does not exist or an error happened - contact admin", "danger")
        return redirect(url_for("boards.my_boards"))
    elif get_board_row.is_shared == True:
        get_userteam_row = UserTeam.query.filter_by(user_id = current_user.id, team_id = get_board_row.team_id).first()
        if get_userteam_row.role != "editor":
            flash("You do not have permission to edit this board. If you believe this is a mistake contact admin.", "danger")
            return redirect(url_for("boards.view_board", board_id = board_id))
    elif get_board_row.is_shared == False:
        if get_board_row.user_id != current_user.id:
            flash("You do not have permission to delete this board. If you want to have it deleted, contact admin.", "danger")
            return redirect(url_for("boards.view_board", board_id = board_id))
    
    # get new name and new color and commit it to DB
    new_name = request.form.get("NEW_NAME_PLACEHOLDER")

    if not new_name:
        flash("Group name cannot be empty", "danger")
        return redirect(url_for("boards.view_board", board_id = board_id))
    
    get_group_row.group_name = new_name

    new_color = request.form.get("NEW_COLOR_PLACEHOLDER")
    get_group_row.group_color = new_color

    db.session.commit()

    flash("Group has been successfully updated!", "success")
    return redirect(url_for("boards.view_board", board_id = board_id))