from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash
from importlib import import_module
from datetime import datetime


class Admin(UserMixin, db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)

    def __repr__(self):
        return "<Admin: {}>".format(self.admin_username)

    @property
    def password(self, password):
        raise AttributeError("password can't be read.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)