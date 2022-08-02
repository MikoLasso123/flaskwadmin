from modules import app, db, bcrypt, models
from flask import render_template, flash, redirect, url_for, request
from flask_user import current_user, login_required, roles_required, UserManager, SQLAlchemyAdapter

from modules.models import UserRoles, Role

from modules.blueprints.admin.admin import admin
from modules.blueprints.users.users import users

app.register_blueprint(admin, url_prefix='/admin/')
app.register_blueprint(users, url_prefix='/users/')

db_adapter = SQLAlchemyAdapter(db, models.Users)
user_manager = UserManager(db_adapter, app)

from modules.utils import get_current_user

@app.route('/')
@app.route('/home')
def home():
    try:
        curr_user = get_current_user(current_user)
    except AttributeError:
        curr_user = None
    return render_template('home.html', title='DemoCompany', current=curr_user)
