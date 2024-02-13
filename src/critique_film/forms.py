from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class InscriptionForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()]) 
    submit = SubmitField('Inscription')
