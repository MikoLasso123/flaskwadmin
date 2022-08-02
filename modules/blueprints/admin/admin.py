from flask import Blueprint, render_template, request, redirect, flash
from flask_user import roles_required, current_user
from modules.models import Users, UserRoles, Role, Company, UserCompanies
from modules import bcrypt, db

from modules.utils import get_current_user

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/users/view')
@admin.route('/users/view/<user_id>')
@roles_required('Admin')
def view_user(user_id=None):
    if user_id:
        user = Users.query.get(int(user_id))
        return render_template('admin/manage_users.html', title='Manage users', user=user)
    else:
        try:
            curr_user = get_current_user(current_user)
        except AttributeError:
            curr_user = None
        users = Users.query.all()
        users_ready = []
        for user in users:
            try:
                user_role = UserRoles.query.filter_by(user_id=user.id).first()
                usr_role = Role.query.get(user_role.role_id)
            except:
                usr_role = None
            usr = {
                'id': user.id,
                'username': user.username,
                'active': user.active,
                'role': usr_role.name
            }
            users_ready.append(usr)
        
        return render_template('admin/manage_users.html', title='Manage users', users=users_ready, current=curr_user)

@admin.route('/users/manage/<action>', methods=['GET', 'POST'])
@admin.route('/users/manage/<action>/<user_id>', methods=['GET', 'POST'])
@roles_required('Admin')
def manage_users(action, user_id=None):
    roles_mapping = {
        '1': 'Admin',
        '2': 'User'
    }
    try:
        curr_user = get_current_user(current_user)
    except AttributeError:
        curr_user = None
    if action == 'new':
        if request.method == 'GET':
            return render_template('admin/new_user_form.html', title='Create new user', current=curr_user)
    
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = Users(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            role = Role.query.filter_by(name=roles_mapping[role]).first()
            new_user_role = UserRoles(user_id=new_user.id, role_id=role.id)
            db.session.add(new_user_role)
            db.session.commit()

            flash('User created', category='success')

            return redirect('/admin/users/view')

    if action == 'update':
        user = Users.query.get(user_id)
        if request.method == 'GET':
            return render_template('admin/edit_user_form.html', title='Create new user', current=curr_user, user=user)

        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user.username = username
            user.password = password
            db.session.commit()

            role = Role.query.filter_by(name=roles_mapping[role]).first()
            user_role = UserRoles.query.filter_by(user_id=user.id).first()
            user_role.role_id = role.id
            db.session.commit()

            flash('User updated', category='success')

            return redirect('/admin/users/view')


    if action == 'disable':
        user = Users.query.get(user_id)
        user.active = False
        db.session.commit()
        flash('User disabled', category='success')
        return redirect('/admin/users/view')
    
    if action == 'enable':
        user = Users.query.get(user_id)
        user.active = True
        db.session.commit()
        flash('User enabled', category='success')
        return redirect('/admin/users/view')
    
    if action == 'delete':
        user = Users.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted', category='success')
        return redirect('/admin/users/view')


@admin.route('/companies/view')
@admin.route('/companies/view/<company_id>')
@roles_required('Admin')
def view_companies(company_id=None):
    if company_id:
        company = Company.query.get(int(company_id))
        return render_template('admin/manage_users.html', title='Manage users', user=user)
    else:
        try:
            curr_user = get_current_user(current_user)
        except AttributeError:
            curr_user = None
        companies = Company.query.all()
        
        return render_template('admin/manage_companies.html', title='Manage users', companies=companies, current=curr_user)

@admin.route('/companies/manage/<action>', methods=['GET', 'POST'])
@admin.route('/companies/manage/<action>/<company_id>', methods=['GET', 'POST'])
@roles_required('Admin')
def manage_companies(action, company_id=None):
    try:
        curr_user = get_current_user(current_user)
    except AttributeError:
        curr_user = None
    if action == 'new':
        if request.method == 'GET':
            return render_template('admin/new_company.html', title='Add new company', current=curr_user)
    
        if request.method == 'POST':
            title = request.form['title']
            discription = request.form['discription']
            new_company = Company(title=title, discription=discription)
            db.session.add(new_company)
            db.session.commit()

            flash('Company created', category='success')

            return redirect('/admin/companies/view')

    if action == 'update':
        company = Company.query.get(int(company_id))
        if request.method == 'GET':
            return render_template('admin/edit_company.html', title='Add new company', current=curr_user, company=company)
    
        if request.method == 'POST':
            title = request.form['title']
            discription = request.form['discription']
            company.title = title
            company.discription = discription
            db.session.commit()

            flash('Company updated', category='success')

            return redirect('/admin/companies/view')
    
    if action == 'delete':
        company = Company.query.get(int(company_id))
        db.session.delete(company)
        db.session.commit()
        flash('Company deleted', category='success')
        return redirect('/admin/companies/view')

@admin.route('/relations', methods=['GET', 'POST'])
@admin.route('/relations/<action>', methods=['GET', 'POST'])
@admin.route('/relations/<action>/<user_id>', methods=['GET', 'POST'])
@roles_required('Admin')
def manage_relations(action, user_id=None):
    try:
        curr_user = get_current_user(current_user)
    except AttributeError:
        curr_user = None
    
    if action == 'view':
        if not user_id:
            users = Users.query.all()
            return render_template('admin/manage_relations.html', current=curr_user, users=users)
        
        if user_id:
            companies = Company.query.all()
            return render_template('admin/choose_companies.html', current=curr_user, companies=companies, user_id=user_id)
    
    if action == 'view_companies':
        user_companies = UserCompanies.query.filter_by(user_id=int(user_id)).all()
        usr_companies = []
        for usr_com in user_companies:
            comp = Company.query.get(usr_com.company_id)
            usr_cmp = {'relation_id': usr_com.id, 'company': comp}
            usr_companies.append(usr_cmp)
        return render_template('admin/edit_relations.html', current=curr_user, companies=usr_companies)

    if action == 'save_relation':
        print(user_id)
        user = Users.query.get(int(user_id))
        print(user.username)
        keys = request.form.keys()
        for key in keys:
            companies = key.split(',')
            for comp_id in companies:
                com = Company.query.get(int(comp_id))
                user.companies.append(com)
        db.session.commit()
        flash('Relation saved', category='success')
        return redirect('/admin/relations/view')
    
    if action == 'delete':
        relation = UserCompanies.query.get(user_id)
        user_id_orig = relation.user_id
        db.session.delete(relation)
        db.session.commit()
        flash('Relation deleted', category='success')
        return redirect(f'/admin/relations/view_companies/{user_id_orig}')