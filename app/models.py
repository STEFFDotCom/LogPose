from app import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    user_name = db.Column(db.String(100), nullable = False, unique = True)
    password_hash = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    is_admin = db.Column(db.Boolean, nullable = False, default = False)

#  retrieve the user from the session with an ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Team(db.Model):
    __tablename__ = "teams"
    
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    team_name = db.Column(db.String(100), nullable = False)

class UserTeam(db.Model):
    __tablename__ = "users_teams"

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    role = db.Column(db.String(100), nullable = False, default = "Viewer")

class Board(db.Model):
    __tablename__ = "boards"

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    board_name = db.Column(db.String(100), nullable = False)
    # if board is personal this is false, if it is shared it is true.
    is_shared = db.Column(db.Boolean, nullable = False, default = False)
    # shared boards have team_id
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable = True)
    # personal boards have users_id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = True)

class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    board_id = db.Column(db.Integer, db.ForeignKey("boards.id"), nullable = False)
    group_name = db.Column(db.String(100), nullable = False)
    group_color = db.Column(db.String(7), nullable = False)
    position = db.Column(db.Integer, nullable = False, default = 1)

class Link(db.Model):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable = False)
    URL = db.Column(db.String(1000), nullable = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(150), nullable = True)
    position = db.Column(db.Integer, nullable = False, default = 1)

class Log(db.Model):
    __tablename__ = "log"

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    action_taken = db.Column(db.String(1000), nullable = False)
    time = db.Column(db.DateTime, nullable = False, default = db.func.now())
