from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Length,Email,NumberRange,ValidationError
from favoriteThings.models import Categories

class CreateCategory(FlaskForm):
    newCategory = StringField("New Category",validators=[DataRequired()])
    rate = IntegerField("Rate",
                        validators=[DataRequired(),NumberRange(min=1)])
    submit = SubmitField('Add')

    def validate_newCategory(self,newCategory):
        category = Categories.query.filter_by(newCategory=newCategory.data).first()
        if category:
            raise ValidationError('Category name Already Exist')