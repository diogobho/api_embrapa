from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField

class UserForms(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=20)])
    nickname = StringField('Username', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha1 = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    senha2 = PasswordField('Confirme a senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    registrar = SubmitField('Registrar')