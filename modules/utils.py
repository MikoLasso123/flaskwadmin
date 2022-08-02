from modules.models import UserRoles, Role

def get_current_user(current_user):
    try:
        user_role = UserRoles.query.filter_by(user_id=current_user.id).first()
        usr_role = Role.query.get(user_role.role_id)
    except:
        usr_role = None
    usr = {
        'id': current_user.id,
        'username': current_user.username,
        'active': current_user.active,
        'role': usr_role.name
    }
    return usr