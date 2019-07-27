from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length

class Create(FlaskForm):
    title = StringField("Name",
                        validators=[DataRequired(),Length(min=2,max=20)])
    description = TextAreaField("Description",
                            validators=[Length(0,150)])
    metadata = TextAreaField("Metadata",
                            validators=[Length(0,150)])
    category=SelectField("Category",
                        validators=[DataRequired()],choices = [])
    newCategory = StringField("New Category")
    
    submit = SubmitField('Add')