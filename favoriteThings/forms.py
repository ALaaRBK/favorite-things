from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),Length(min=4,max=20)]) 
    email = StringField("Email",
                        validators=[DataRequired(),Email()])
    password = PasswordField("Password",
                            validators=[DataRequired()])

    submit = SubmitField('Sign UP')

class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(),Email()])
    password = PasswordField("Password",
                            validators=[DataRequired()])
    remmber = BooleanField('Remmber Me')
    submit = SubmitField('Login')
