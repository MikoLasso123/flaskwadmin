from modules import db, bcrypt
from modules.models import Users, UserRoles, Role, Company
import faker
import os
import hashlib

fake = faker.Faker()

class DatabaseBuilder:
    def __init__(self):
        self.db_path = os.path.join('modules', 'site.db')

    def check_for_db(self):
        db_set = False
        if os.path.isfile(self.db_path):
            db_set = True
        return db_set
    
    def create_db(self):
        db_set = self.check_for_db()
        if db_set:
            db.drop_all()
            db.create_all()
        else:
            db.create_all()
    
    def make_admin(self):
        hashed_pass = bcrypt.generate_password_hash('root23')
        user = Users(username='root23', password=hashed_pass)
        db.session.add(user)
        admin_role = Role(name='Admin')
        user_role = Role(name='User')
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()
        userRole = UserRoles(user.id, admin_role.id)
        db.session.add(userRole)
        db.session.commit()
    
    def make_users(self):
        for _ in range(10):
            username = fake.simple_profile()
            username = username['username']
            print(f'Generated {username}')
            hashed_pass = bcrypt.generate_password_hash(username)
            fake_user = Users(username=username, password=hashed_pass)
            db.session.add(fake_user)
            db.session.commit()
            fake_user_role = UserRoles(fake_user.id, 2)
            db.session.add(fake_user_role)
            db.session.commit()
    
    def hash_disc(self, string):
        hashed_string = hashlib.sha256(string.encode('utf-8')).hexdigest()
        return hashed_string
    
    def make_companies(self):
        for _ in range(50):
            fake_company_name = fake.company()
            fake_discription = self.hash_disc(fake_company_name)
            print(f'Generated company {fake_company_name}')
            fake_company = Company(title=fake_company_name, discription=fake_discription)
            db.session.add(fake_company)
            db.session.commit()



def make_db():
    print('Creating database')
    db_maker = DatabaseBuilder()
    db_maker.create_db()
    db_maker.make_admin()
    db_maker.make_users()
    db_maker.make_companies()
    print('Done')

if __name__ == '__main__':
    make_db()