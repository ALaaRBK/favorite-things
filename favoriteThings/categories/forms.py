from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField
from wtforms.validators import DataRequired,NumberRange

class CreateCategory(FlaskForm):
    newCategory = StringField("New Category",validators=[DataRequired()])
    rate = IntegerField("Rate",
                        validators=[DataRequired(),NumberRange(min=1)])
    submit = SubmitField('Add')