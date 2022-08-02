from modules import db
from flask_user import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), default=False, server_default='0')
    roles = db.relationship('Role', secondary='user_roles')
    companies = db.relationship('Company', secondary='user_companies')

    def __init__(self, username, password, active=True):
        self.username = username
        self.password = password
        self.active = active

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50))
    discription = db.Column(db.String(600))

    def __init__(self, title, discription):
        self.title = title
        self.discription = discription

class UserCompanies(db.Model):
    __tablename__ = 'user_companies'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    company_id = db.Column(db.Integer(), db.ForeignKey('companies.id', ondelete='CASCADE'))