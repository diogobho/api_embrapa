from flask import Flask, render_template, request
from web_scraping_py.producao import scrape_viti_producao
from web_scraping_py.comercializacao import scrape_viti_comercializacao

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', 
                           titulo='Embrapa - Vitivicultura')


@app.route('/producao', methods=['POST', 'GET'])
def producao():
    if request.method == 'POST':
        user_year = int(request.form['ano'])

        df = scrape_viti_producao(user_year)
        df_html = df.to_html(index=False)

        return render_template('producao.html', 
                                table=df_html, 
                                user_year=user_year, 
                                titulo=' Embrapa - Produção',
                                nome = 'Produção')
    
    elif request.method == 'GET':
        return render_template('producao.html', 
                               table=None, 
                               titulo=' Embrapa - Produção', 
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
                               titulo=' Embrapa - Comercialização', 
                               nome = 'Comercialização')
    
    elif request.method == 'GET':
        return render_template('producao.html', 
                               table=None, 
                               titulo=' Embrapa - Comercialização', 
                               nome = 'Comercialização')

if __name__ == "__main__":
    app.run(debug=True)