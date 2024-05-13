from flask import Flask, render_template, request
from web_scraping_py.producao import scrape_viti_brasil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', titulo='Embrapa')


@app.route('/producao', methods=['POST', 'GET'])
def producao():

    if request.method == 'POST':
        user_year = int(request.form['ano'])

        df = scrape_viti_brasil(user_year)
        df_html = df.to_html(index=False)

        return render_template('producao.html', table=df_html, user_year=user_year, titulo=' Embrapa - Produção')
    
    elif request.method == 'GET':
        return render_template('producao.html', table=None, titulo=' Embrapa - Produção')

# @app.route('/comercializacao')
# def comercializacao():
#     return render_template('comercializacao.html')

# @app.route('/processamento')
# def processamento():
#     return render_template('processamento.html')

# @app.route('/importacao')
# def importacao():
#     return render_template('importacao.html')

# @app.route('/exportacao')
# def exportacao():
#     return render_template('exportacao.html')


if __name__ == "__main__":
    app.run(debug=True)