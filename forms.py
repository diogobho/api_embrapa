from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired

class UserForms(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=20)])
    nickname = StringField('Username', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha1 = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    senha2 = PasswordField('Confirme a senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    registrar = SubmitField('Registrar')

class LoginForms(FlaskForm):
    nickname = StringField('Username', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

class AnoForms(FlaskForm):
    ano2022 = SelectField('Escolha o ano (1970 - 2022):', choices=[(str(year), str(year)) for year in range(1970, 2023)], validators=[DataRequired()], default=2022)
    ano2023 = SelectField('Escolha o ano (1970 - 2023):', choices=[(str(year), str(year)) for year in range(1970, 2024)], validators=[DataRequired()], default=2023)
    submit = SubmitField('Buscar')