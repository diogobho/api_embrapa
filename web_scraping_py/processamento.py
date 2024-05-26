import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_viti_processamento(ano, opcao):
    def extrair_subopcoes(conteudo_html):
        sopa = BeautifulSoup(conteudo_html, 'html.parser')
        botoes = sopa.find_all('button', class_='btn_sopt')
        return {botao['value']: botao.get_text(strip=True) for botao in botoes}

    def processar_tabela(sopa, opcao, ano, produto_principal):
        tabela = sopa.find('table', class_='tb_dados')
        if not tabela:
            return None

        dados = []
        linhas = tabela.find_all('tr')[1:]  # Ignora o cabeçalho
        for linha in linhas:
            celulas = linha.find_all('td')
            if not celulas:
                continue

            classe_celula = celulas[0].get('class', [])
            produto = celulas[0].get_text(strip=True)
            quantidade = celulas[1].get_text(strip=True)

            if 'tb_item' in classe_celula:
                dados.append({
                    'tabela': dicionario_opcao[opcao],
                    'produto': produto,
                    'sub_produto': None,
                    'quantidade': quantidade,
                    'ano': ano,
                    'unidade_medida': 'kg'
                })
            elif 'tb_subitem' in classe_celula:
                dados.append({
                    'tabela': dicionario_opcao[opcao],
                    'produto': produto_principal,
                    'sub_produto': produto,
                    'quantidade': quantidade,
                    'ano': ano,
                    'unidade_medida': 'kg'
                })

        df = pd.DataFrame(dados)
        return df.dropna(subset=['sub_produto'])

    dicionario_opcao = {'opt_03': 'Processamento'}
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opcao}'
    resposta = requests.get(url)
    
    if resposta.status_code != 200:
        print('Falha ao fazer a solicitação HTTP para a página principal.')
        return None

    mapeamento_subopcao = extrair_subopcoes(resposta.content)
    lista_dfs = []

    for subopcao, produto_principal in mapeamento_subopcao.items():
        sub_url = f'{url}&subopcao={subopcao}'
        sub_resposta = requests.get(sub_url)
        
        if sub_resposta.status_code != 200:
            print(f'Falha ao fazer a solicitação HTTP para subopção {subopcao}.')
            continue
        
        sub_sopa = BeautifulSoup(sub_resposta.content, 'html.parser')
        df = processar_tabela(sub_sopa, opcao, ano, produto_principal)
        if df is not None:
            lista_dfs.append(df)
        else:
            print(f'Tabela não encontrada para subopção {subopcao}.')

    if lista_dfs:
        return pd.concat(lista_dfs, ignore_index=True)
    else:
        return None
