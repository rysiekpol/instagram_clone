from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    photo = FileField('Upload Photo', validators=[FileRequired('File field should not be empty'), FileAllowed(['jpg', 'png'], 'Images only!')])
    description = TextAreaField('Describe your image', validators=[DataRequired()])
    submit = SubmitField('Submit')