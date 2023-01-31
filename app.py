import string
import random
from flask_admin.contrib.sqla import ModelView
from flask_restful import Api, Resource
from flask import Flask, request
from model_views import (
    testAdminView, testUserView, MyModelView, usernameview, testView1, samplep, invoice, report
)
import forms
import os
from flask import (Flask, url_for, render_template,
                   abort, redirect
                   )
from flask_sqlalchemy import SQLAlchemy
from flask_security import (Security, SQLAlchemyUserDatastore,
                            UserMixin, RoleMixin, login_required, current_user, roles_required
                            )
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin import BaseView
from flask_admin import helpers as admin_helpers
from flask_admin.contrib import sqla
from datetime import datetime


def create_app():
    # The template files will be stored in the [templates] directory
    app = Flask(__name__, template_folder="templates")
    app.debug = True
    app.config.from_pyfile('config.py')
    return app


# Construct an instance of Flask class for our webapp
app = create_app()
# Create database connection object
db = SQLAlchemy(app)
app.app_context().push()
# --------------------------------
# FLASK-SECURITY MODELS
# --------------------------------
user_profiles = db.Table(
    'profile_username',
    db.Column('username_id', db.Integer(), db.ForeignKey('username.id')),
    db.Column('profile_id', db.Integer(), db.ForeignKey('profile.id'))
)


class Profile(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class Username(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Profile',
                            secondary=user_profiles,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


# --------------------------------
# FORMS
# --------------------------------

# --------------------------------
# Setup Flask-Security
# --------------------------------
user_datastore = SQLAlchemyUserDatastore(db, Username, Profile)
security = Security(app, user_datastore,
                    login_form=forms.ExtendedLoginForm)
# register_form=forms.ExtendedRegisterForm)

# --------------------------------
# MODELS
# --------------------------------


class test(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(50))
    date = db.Column(db.Date())
    Clinic_ReferralName = db.Column(db.String(50))
    Location = db.Column(db.String(50))
    Breed = db.Column(db.String(50))
    Sample = db.Column(db.String(50))
    Species = db.Column(db.String(50))
    Age = db.Column(db.Integer)
    Owner = db.Column(db.String(50))
    Mobile = db.Column(db.String(50))
    Tests = db.Column(db.String(50))

    def __str__(self):
        return self.desc


class usertest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(50))


# --------------------------------
# MODEL VIEW CLASSES
# --------------------------------

# --------------------------------
# FLASK VIEWS / ROUTES
# --------------------------------

@app.route('/')
def index():
    # return render_template('index.html')
    return redirect("/admin")


# --------------------------------
# CREATE FLASK ADMIN
# --------------------------------
admin = flask_admin.Admin(
    app,
    '',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# visible only for admin
admin.add_view(MyModelView(Profile, db.session))
admin.add_view(usernameview(Username, db.session))

# visible for users and admin

# manage sample tab
admin.add_view(testUserView(name="Create Order",
               endpoint='usertest', category='Manage Orders'))
admin.add_view(testAdminView(test, db.session,
               name="Order History", category="Manage Orders"))
# admin.add_view(testView1(name="Legacy Sample Request",category='Manage Orders'))

# Sample Tracking tab
admin.add_view(samplep(name="Sample Pickup", category='Sample Tracking'))


# Invoice tab
admin.add_view(invoice(name="Invoice1", category='Inovice'))

# Report tab
admin.add_view(report(name="Report1", category="Report"))


#
#
#
#





def process_data(data,testId):
    # do something with the data
    # username = request.form['uname']
    try:
        checkTestId = test.query.filter_by(id=testId).first()
        if (checkTestId != None):
            generate_id(data)
        desc=data['address']
        current_time = datetime.now()
        clinic = data['clinicname']
        loaction = data['state']
        breed = data['breed']
        sample = data['sample']
        species = data['species']
        age = data['age']
        owner = data['username']
        mobile = data['phno']
        tests = data['testBox1']
        testDb = test(id=testId, desc=desc, date=current_time,
                      Clinic_ReferralName=clinic, Location=loaction, Breed=breed, Sample=sample, Species=species, Age=age, Owner=owner, Mobile=mobile, Tests=tests)
        db.session.add(testDb)
        db.session.commit()
        return
    except:
        return render_template('admin/usertest.html')


def generate_id(data):
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    process_data(data, id)
    return
#
#
#
#
#


# --------------------------------
# define a context processor for merging flask-admin's template context
#   into the flask-security views.
# --------------------------------
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

# --------------------------------
# Populate a small db with some example entries.
# --------------------------------


def build_sample_db():
    import string
    import random

    db.drop_all()
    db.create_all()

    with app.app_context():
        profile_user = Profile(name='user')
        profile_super_user = Profile(name='superuser')
        db.session.add(profile_user)
        db.session.add(profile_super_user)
        db.session.commit()

        test_user = user_datastore.create_user(
            first_name='Admin',
            username='admin',
            email='admin@test.com',
            password=encrypt_password('admin'),
            roles=[profile_super_user]
        )

        first_names = [
            'Anand', 'Preethi', 'Jon'
        ]
        last_names = [
            'Choudhary', 'P', 'Snow'
        ]

        for i in range(len(first_names)):
            tmp_email = "{}.{}@test.com".format(first_names[i].lower(),
                                                last_names[i].lower())
            tmp_pass = (str(first_names[i]+last_names[i])).lower()
            user_datastore.create_user(
                first_name=first_names[i],
                last_name=last_names[i],
                username=first_names[i].lower(),
                email=tmp_email,
                password=encrypt_password(tmp_pass),
                roles=[profile_user],
                confirmed_at=datetime.now()

            )
        db.session.commit()
    return


# --------------------------------
# MAIN APP
# --------------------------------
if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    # db.create_all()
    ##    app_dir = os.path.realpath(os.path.dirname(__file__))
    ##    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    # if not os.path.exists(database_path):
    # build_sample_db()

    app.run()