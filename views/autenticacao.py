from flask import render_template, request, redirect, session, flash, url_for
from embrapa import app, db
from models import Usuarios
from forms import UserForms, LoginForms
from flask_bcrypt import check_password_hash, generate_password_hash

@app.route('/login')
def login():

    proxima = request.args.get('proxima', url_for('producao'))

    form = LoginForms()
    
    return render_template('login.html', proxima=proxima , nome = 'Login', form=form)

@app.route('/autenticar', methods=['POST', 'GET'])
def autenticar():
    
    form = LoginForms(request.form)

    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()

    senha = check_password_hash(usuario.senha, form.senha.data)

    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname.capitalize() + ' logou com sucesso!', 'success')
        proxima_pag = request.form['proxima']
        return redirect(proxima_pag)
    else:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():

    session.pop('usuario_logado', None) 
    flash('Usuário deslogado com sucesso!', 'success')

    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    proxima = request.args.get('proxima', url_for('register'))

    form = UserForms()

    if request.method == 'POST' and form.validate_on_submit():
        nome = form.nome.data
        nickname = form.nickname.data
        senha1 = form.senha1.data
        senha2 = form.senha2.data

        if senha1 != senha2:
            flash('Senhas não coincidem.', 'error')
            return redirect(url_for('register'))

        try:
            senha_hash = generate_password_hash(senha1).decode('utf-8')
            novo_usuario = Usuarios(nome=nome, nickname=nickname, senha=senha_hash)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário registrado com sucesso!', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            flash('Erro ao registrar o usuário. Tente novamente.', 'error')

    return render_template('register.html', titulo='Registro de usuários', nome='Registro', proxima=proxima, form=form)
