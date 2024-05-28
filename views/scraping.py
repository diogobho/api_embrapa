from flask import render_template, request, redirect, session, url_for, flash
from main import app
from web_scraping_py.producao import scrape_viti_producao
from web_scraping_py.comercializacao import scrape_viti_comercializacao
from web_scraping_py.processamento import scrape_viti_processamento
from web_scraping_py.importacao_exportacao  import scrape_viti_imp_exp
from forms import AnoForms

@app.route('/producao', methods=['POST', 'GET'])
def producao():

    form = AnoForms(request.form)

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',
                                proxima=url_for('producao')))

    if request.method == 'POST' and form.validate_on_submit():
        user_year = int(form.ano2022.data)
        try:
            df = scrape_viti_producao(user_year)
            df_html = df.to_html(index=False)

            return render_template('producao.html', 
                                    table=df_html, 
                                    user_year=user_year, 
                                    nome = 'Produção',
                                    form = form)
        except Exception as e:
            flash('Erro ao obter os dados da tabela de Produção')
            return render_template('producao.html', table=None, nome='Produção', form=form)
    
    return render_template('producao.html', table=None, nome='Produção', form=form)

    
@app.route('/comercializacao', methods=['POST', 'GET'])
def comercializacao():

    form = AnoForms(request.form)

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', 
                                proxima=url_for('comercializacao')))

    if request.method == 'POST':
        user_year = int(form.ano2022.data)

        df = scrape_viti_comercializacao(user_year)
        df_html = df.to_html(index=False)

        return render_template('comercializacao.html', 
                               table=df_html, 
                               user_year=user_year,  
                               nome = 'Comercialização',
                               form = form)
    
    elif request.method == 'GET':
        return render_template('comercializacao.html', 
                               table=None,  
                               nome = 'Comercialização',
                               form = form)
    
@app.route('/processamento', methods=['POST', 'GET'])
def processamento():

    form = AnoForms(request.form)

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',
                                proxima=url_for('processamento')))
    
    if request.method == 'POST':
        user_year = int(form.ano2022.data)

        df = scrape_viti_processamento(user_year, 'opt_03')
        df_html = df.to_html(index=False)

        return render_template('processamento.html', 
                               table=df_html, 
                               user_year=user_year,  
                               nome = 'Processamento',
                               form = form)
    
    elif request.method == 'GET':
        return render_template('processamento.html', 
                               table=None,  
                               nome = 'Processamento',
                               form = form)
        
@app.route('/importacao', methods=['POST', 'GET'])
def importacao():

    form = AnoForms(request.form)

    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', 
                                proxima=url_for('comercializacao')))

    if request.method == 'POST':
        user_year = int(form.ano2023.data)

        df = scrape_viti_imp_exp(user_year, 'opt_05')
        if df is not None:
            df_html = df.to_html(index=False)
            return render_template('importacao.html', 
                                   table=df_html, 
                                   user_year=user_year, 
                                   nome='Importação',
                                   form = form)
        else:
            return render_template('importacao.html', 
                                   error_message='Falha ao obter os dados de importação.', 
                                   nome='Importação',
                                   form = form)

    # Caso o método seja GET, renderizar a página padrão
    return render_template('importacao.html', 
                           nome='Importação', 
                           form = form)
        
@app.route('/exportacao', methods=['POST', 'GET'])
def exportacao():

    form = AnoForms(request.form)

    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', 
                                proxima=url_for('comercializacao')))

    if request.method == 'POST':
        user_year = int(form.ano2023.data)

        df = scrape_viti_imp_exp(user_year, 'opt_06')
        if df is not None:
            df_html = df.to_html(index=False)
            return render_template('exportacao.html', 
                                   table=df_html, 
                                   user_year=user_year, 
                                   nome='Exportação', 
                                   form=form)
        else:
            return render_template('exportacao.html', 
                                   error_message='Falha ao obter os dados de exportação.', 
                                   nome='Exportação', 
                                   form=form)

    # Caso o método seja GET, renderizar a página padrão
    return render_template('exportacao.html',
                           nome='Exportação', 
                           form=form)