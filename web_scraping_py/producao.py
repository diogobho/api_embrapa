import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_viti_brasil(year):
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02'

    response = requests.get(url)

    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        tabela = 'Producao'
        produto = ''
        sub_produto = ''
        quantidade = ''
        ano = str(year)  
        unidade_medida = 'Litro'  

        rows = soup.find_all('tr')

        for row in rows:
            
            cells = row.find_all('td')
            
            if cells:
                
                if 'tb_item' in cells[0].get('class', []):
                    produto = cells[0].get_text(strip=True)
                    quantidade = cells[1].get_text(strip=True)
                    
                    data.append({'tabela': tabela, 'produto': produto, 'quantidade': quantidade, 'ano': ano, 'unidade_medida': unidade_medida})
                
                elif 'tb_subitem' in cells[0].get('class', []):
                    sub_produto = cells[0].get_text(strip=True)
                    quantidade = cells[1].get_text(strip=True)
                    
                    data.append({'tabela': tabela, 'produto': produto, 'sub_produto': sub_produto, 'quantidade': quantidade, 'ano': ano, 'unidade_medida': unidade_medida})

    else:
        print('Falha ao acessar o site.')

    df = pd.DataFrame(data)
    #alteração feita para excluir os valores nulos da coluna sub_produto
    df = df.dropna(subset=['sub_produto'])
    df = df[['tabela', 'produto', 'sub_produto', 'quantidade', 'ano', 'unidade_medida']]
    return pd.DataFrame(df)
