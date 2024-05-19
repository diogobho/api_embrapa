from flask import Flask, render_template, request, redirect, session, flash, url_for
from web_scraping_py.producao import scrape_viti_producao
from web_scraping_py.comercializacao import scrape_viti_comercializacao
from web_scraping_py.processamento import scrape_viti_processamento
from web_scraping_py.importacao_exportacao  import scrape_viti_imp_exp

app = Flask(__name__)
app.secret_key = 'embrapa'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/producao', methods=['POST', 'GET'])
def producao():

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('producao')))

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
    
@app.route('/comercializacao', methods=['POST', 'GET'])
def comercializacao():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('comercializacao')))

    if request.method == 'POST':
        user_year = int(request.form['ano'])

        df = scrape_viti_comercializacao(user_year)
        df_html = df.to_html(index=False)

        return render_template('comercializacao.html', 
                               table=df_html, 
                               user_year=user_year,  
                               nome = 'Comercialização')
    
    elif request.method == 'GET':
        return render_template('comercializacao.html', 
                               table=None,  
                               nome = 'Comercialização')
    
@app.route('/processamento', methods=['POST', 'GET'])
def processamento():

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('processamento')))
    
    if request.method == 'POST':
        user_year = int(request.form['ano'])
        user_option = request.form['opcao']

        df = scrape_viti_processamento(user_year, user_option)
        df_html = df.to_html(index=False)

        return render_template('processamento.html', 
                               table=df_html, 
                               user_year=user_year,  
                               nome = 'Processamento')
    
    elif request.method == 'GET':
        return render_template('processamento.html', 
                               table=None,  
                               nome = 'Processamento')
        
@app.route('/importacao', methods=['POST', 'GET'])
def importacao():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('comercializacao')))

    if request.method == 'POST':
        user_year = int(request.form['ano'])

        df = scrape_viti_imp_exp(user_year, 'opt_05')
        if df is not None:
            df_html = df.to_html(index=False)
            return render_template('importacao.html', table=df_html, user_year=user_year, nome='Importação')
        else:
            return render_template('importacao.html', error_message='Falha ao obter os dados de importação.', nome='Importação')

    # Caso o método seja GET, renderizar a página padrão
    return render_template('importacao.html', nome='Importação')
        
@app.route('/exportacao', methods=['POST', 'GET'])
def exportacao():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('comercializacao')))

    if request.method == 'POST':
        user_year = int(request.form['ano'])

        df = scrape_viti_imp_exp(user_year, 'opt_06')
        if df is not None:
            df_html = df.to_html(index=False)
            return render_template('exportacao.html', table=df_html, user_year=user_year, nome='Exportação')
        else:
            return render_template('exportacao.html', error_message='Falha ao obter os dados de exportação.', nome='Exportação')

    # Caso o método seja GET, renderizar a página padrão
    return render_template('exportacao.html', nome='Exportação')

    
# ROTAS PARA AUTENTICAÇÃO
@app.route('/login')
def login():
    proxima = request.args.get('proxima', url_for('index'))

    if 'usuario_logado' in session:
        flash('Você já está logado.', 'info')
        return redirect(url_for('index'))
    
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():

    if 'teste' == request.form['senha']:

        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ' logado com sucesso!', 'success')

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

if __name__ == "__main__":
    app.run(debug=True)