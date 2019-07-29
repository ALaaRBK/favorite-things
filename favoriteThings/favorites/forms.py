from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length,ValidationError
from favoriteThings.models import Categories
class Create(FlaskForm):

    title = StringField("Name",
                        validators=[DataRequired(),Length(min=2,max=30)])
    description = TextAreaField("Description")
    metadata = TextAreaField("Metadata")
    category=SelectField("Category",
                         validators=[DataRequired()])
    newCategory = StringField("New Category")
    
    submit = SubmitField('Add')

    def validate_description(self,description):
        print(len(description.data))
        if description.data:
            if len(description.data) < 10:
                raise ValidationError('Description Field must be minimum 10 and 20 characters long')

