from flask import Flask, render_template, request, redirect, session, flash
from web_scraping_py.producao import scrape_viti_producao
from web_scraping_py.comercializacao import scrape_viti_comercializacao

app = Flask(__name__)
app.secret_key = 'embrapa'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/producao', methods=['POST', 'GET'])
def producao():
    if request.method == 'POST':
        user_year = int(request.form['ano'])

        df = scrape_viti_producao(user_year)
        df_html = df.to_html(index=False)

        return render_template('producao.html', 
                                table=df_html, 
                                user_year=user_year, 
                                nome = 'Produção')
    
    elif request.method == 'GET':
        return render_template('producao.html', 
                               table=None,  
                               nome = 'Produção')
    
@app.route('/comercialização', methods=['POST', 'GET'])
def comercializacao():
    if request.method == 'POST':
        user_year = int(request.form['ano'])

        df = scrape_viti_comercializacao(user_year)
        df_html = df.to_html(index=False)

        return render_template('comercializacao.html', 
                               table=df_html, 
                               user_year=user_year,  
                               nome = 'Comercialização')
    
    elif request.method == 'GET':
        return render_template('producao.html', 
                               table=None,  
                               nome = 'Comercialização')
    
# ROTAS PARA AUTENTICAÇÃO
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST','GET'])
def autenticar():
    if 'teste' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ' logado com sucesso!')
        return redirect('/')
    else:
        flash('Login não efetuado.')
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogado com sucesso.')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)