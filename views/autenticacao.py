from flask import render_template, request, redirect, session, flash, url_for
from embrapa import app, db
from models import Usuarios
from forms import UserForms

@app.route('/login')
def login():
    proxima = request.args.get('proxima', url_for('index'))

    if 'usuario_logado' in session:
        flash('Você já está logado.', 'info')
        return redirect(url_for('index'))
    
    return render_template('login.html', proxima=proxima , nome = 'Login')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logou com sucesso!', 'success')
            proxima_pag = request.form.get('proxima', url_for('index'))
            return redirect(proxima_pag)
        
        else:

            flash('Login não efetuado.', 'error')
            return redirect(url_for('login'))
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
            novo_usuario = Usuarios(nome=nome, nickname=nickname, senha=senha1)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário registrado com sucesso!', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            flash('Erro ao registrar o usuário. Tente novamente.', 'error')

    return render_template('register.html', titulo='Registro de usuários', nome='Registro', proxima=proxima, form=form)
