import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_viti_imp_exp(ano, opcao):
    opcao_dict = {'opt_05': 'Importação', 'opt_06': 'Exportação'}

    def extract_suboptions(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        buttons = soup.find_all('button', class_='btn_sopt')
        subopcao_mapping = {}
        for button in buttons:
            subopcao = button['value']
            nome_produto = button.get_text(strip=True)
            subopcao_mapping[subopcao] = nome_produto
        return subopcao_mapping

    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opcao}'
    response = requests.get(url)
    
    if response.status_code == 200:
        subopcao_mapping = extract_suboptions(response.content)
        dfs = []
        for subopcao, produto in subopcao_mapping.items():
            sub_url = f'{url}&subopcao={subopcao}'
            sub_response = requests.get(sub_url)
            if sub_response.status_code == 200:
                sub_soup = BeautifulSoup(sub_response.content, 'html.parser')
                table = sub_soup.find('table', class_='tb_dados')
                if table:
                    data = []
                    rows = table.find_all('tr')
                    for row in rows[1:]:
                        cells = row.find_all('td')
                        row_data = [cell.get_text(strip=True) for cell in cells]
                        data.append(row_data)
                    df = pd.DataFrame(data, columns=['paises', 'quantidade', 'valor'])
                    df['Tabela'] = opcao_dict[opcao]
                    df['Produto'] = produto
                    df['Ano'] = ano
                    df['Unidade_quantidade'] = 'kg'
                    df['Unidade_valor'] = 'US$'
                    df = df[['Tabela', 'Produto', 'paises', 'Ano', 'quantidade', 'Unidade_quantidade', 'valor', 'Unidade_valor']]
                    dfs.append(df)
                else:
                    print(f'Tabela não encontrada para subopcao {subopcao}.')
            else:
                print(f'Falha ao fazer a solicitação HTTP para subopcao {subopcao}.')
        
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        else:
            print('Nenhum dataframe foi criado.')
            return None
    else:
        print('Falha ao fazer a solicitação HTTP para a página principal.')
        return None
