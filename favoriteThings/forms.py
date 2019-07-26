from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,ValidationError
from favoriteThings.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),Length(min=4,max=20)]) 
    email = StringField("Email",
                        validators=[DataRequired(),Email()])
    password = PasswordField("Password",
                            validators=[DataRequired()])

    submit = SubmitField('Sign UP')
    #check if username is already Exist when call  validate_on_submit method
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User Already Exist')
    #check if email is already Exist when call  validate_on_submit method
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Already Exist')

class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(),Email()])
    password = PasswordField("Password",
                            validators=[DataRequired()])
    remmber = BooleanField('Remmber Me')
    submit = SubmitField('Login')
