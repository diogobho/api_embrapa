from flask import render_template, request, redirect, session, flash, url_for
from embrapa import app, db
from models import Usuarios

@app.route('/login')
def login():
    proxima = request.args.get('proxima', url_for('index'))

    if 'usuario_logado' in session:
        flash('Você já está logado.', 'info')
        return redirect(url_for('index'))
    
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logou com sucesso.', 'success')
            proxima_pag = request.form.get('proxima', url_for('index'))
            return redirect(proxima_pag)
        
        else:

            flash('Login não efetuado.', 'error')
            return redirect(url_for('login'))
    
@app.route('/logout')
def logout():

    session.pop('usuario_logado', None) 
    flash('Usuário deslogado com sucesso.', 'success')

    return redirect(url_for('login'))