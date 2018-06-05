from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    admin = StringField("Username", validators=[DataRequired(),
                                                Length(3, 20)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")