from flask import Blueprint, render_template, redirect, request
from modules.models import Company, UserCompanies
from flask_user import roles_required, current_user
from modules.utils import get_current_user

users = Blueprint('users', __name__, template_folder='templates')

@users.route('/companies')
@users.route('/companies/<company_id>')
def company_view(company_id=None):
    try:
        curr_user = get_current_user(current_user)
    except AttributeError:
        curr_user = None

    if company_id:
        company = Company.query.get(int(company_id))
        return render_template('users/company_details.html', title=f'View company {company.title}', company=company, current=curr_user)
    else:
        ready_companies = []
        user_companies = UserCompanies.query.filter_by(user_id=current_user.id).all()
        for comp in user_companies:
            comp_id = comp.company_id
            com = Company.query.get(comp_id)
            ready_companies.append(com)
        
        return render_template('users/companies.html', title='Manage users', companies=ready_companies, current=curr_user)