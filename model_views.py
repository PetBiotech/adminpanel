import datetime
from flask_admin.contrib import sqla
from flask_security import current_user
from flask import Flask, abort, redirect, render_template, url_for, request
from flask_admin import BaseView, expose
import sqlite3
import string
import random

from flask_sqlalchemy import SQLAlchemy
# from app import generate_id,process_data

# from app import generate_id

app = Flask(__name__)


class MyModelView(sqla.ModelView):
    
    @expose("/submit",methods=["POST"])
    def submit(self):
        data=request.form
        print(data)
        print("Here I am")
        return redirect("/successForm")

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser'):
            return True
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users
          when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


@app.route("/successForm")
def successForm():
    print("Happy Stores")


class usernameview(MyModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser'):

            if current_user.has_role('superuser'):
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
                self.can_export = True

            return True
        return False

    column_list = ('id', 'first_name', 'last_name', 'username',
                   'email', 'active', 'roles', 'confirmed_at')


class testUserView(BaseView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    @expose('/')
    def index(self):
        return self.render('admin/usertest.html')

    # column_display_pk = True
    # form_columns = ['id', 'desc']
    # column_searchable_list = ['desc']
    # column_filters = ['id']
    # can_create = True
    # can_edit = True
    # can_delete = False  # disable model deletion
    # can_view_details = True
    # page_size = 50  # pagination
    # create_modal = True
    # edit_modal = True
    # can_export = True


class testAdminView(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            if current_user.has_role('user'):
                self.can_create = False
                self.can_edit = True
                self.can_delete = False
                self.can_export = True
            else:
                self.can_create = False
                self.can_edit = True
                self.can_delete = True
                self.can_export = True
            return True
        return False
    column_display_pk = True
    #form_columns = ['id', 'desc']
    column_searchable_list = ['desc']
    column_filters = ['id']
    column_editable_list = ['desc']
    can_create = False
    can_edit = True

    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True


class testView1(BaseView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    @expose('/')
    def index(self):
        return self.render('admin/legacysr.html')


class samplep(BaseView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    @expose('/')
    def index(self):
        return self.render('admin/samplep.html')


# invoice section

class invoice(BaseView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    @expose('/')
    def index(self):
        return self.render('admin/invoice.html')


# invoice section


class report(BaseView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    @expose('/')
    def index(self):
        return self.render('admin/report.html')

    @expose('/')
    def index(self):
        return self.render('admin/hi.html')
