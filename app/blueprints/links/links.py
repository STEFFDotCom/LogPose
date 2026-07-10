from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Board, UserTeam, Group, Link
from sqlalchemy import func, select

links = Blueprint("links", __name__)

@links.route("/groups/<int:group_id>/links/create", methods=["POST"])
@login_required
def create_link(group_id):
    
    # get row of pressed group
    get_group_row = Group.query.filter_by(id = group_id).first()

    # check if group exists and fetch board id
    if get_group_row:
        board_id = get_group_row.board_id
    else:
        flash("Group does not exist", "danger")
        return redirect(url_for("boards.my_boards"))
    
    # get board row belonging to pressed group
    get_board_row = Board.query.filter_by(id = board_id).first()

    # DEFENSIVE GUARD
    if not get_board_row:
        flash("Group does not exist or an error happened - contact admin", "danger")
        return redirect(url_for("boards.view_board", board_id = board_id))
    elif get_board_row.is_shared == True:
        get_userteam_row = UserTeam.query.filter_by(user_id = current_user.id, team_id = get_board_row.team_id).first()
        if get_userteam_row.role != "editor":
            flash("You do not have permission to create a link on this board. If you want to this access, contact admin.", "danger")
            return redirect(url_for("boards.view_board", board_id = board_id))
    elif get_board_row.is_shared == False:
        if get_board_row.user_id != current_user.id:
            flash("You do not have permission to create a link for this board. If this is your board, contact admin.", "danger")
            return redirect(url_for("boards.view_board", board_id = board_id))

    # create and add link to group
    link_url = request.form.get("link_url")
    link_title = request.form.get("link_title")
    link_description = request.form.get("link_description")

    query_max_position = select(func.max(Link.position)).where(Link.group_id == group_id)
    max_position = db.session.scalar(query_max_position)

    new_link = Link(
        group_id = get_group_row.id,
        URL = link_url,
        title = link_title,
        description = link_description,
        position = (max_position + 1) if max_position is not None else 1
    )

    db.session.add(new_link)
    db.session.commit()
    flash("Link has been created!", "success")
    return redirect(url_for("boards.view_board", board_id = board_id))

@links.route("/links/<int:link_id>/delete", methods = ["POST"])
@login_required
def delete_link(link_id):
    pass

@links.route("/links/<int:link_id>/edit", methods = ["POST"])
@login_required
def edit_link(link_id):
    pass