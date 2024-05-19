import requests
from bs4 import BeautifulSoup
import pandas as pd

def extrair_subopcoes(conteudo_html):
    sopa = BeautifulSoup(conteudo_html, 'html.parser')
    botoes = sopa.find_all('button', class_='btn_sopt')
    mapeamento_subopcao = {}
    for botao in botoes:
        subopcao = botao['value']
        nome_produto = botao.get_text(strip=True)
        mapeamento_subopcao[subopcao] = nome_produto
    return mapeamento_subopcao

def scrape_viti_processamento(ano, opcao):
    dicionario_opcao = {
        'viniferas': 'subopt_01',
        'americanas_hibridas': 'subopt_02',
        'uvas_mesa': 'subopt_03',
        'sem_classificacao': 'subopt_04'
    }

    if opcao not in dicionario_opcao:
        print(f'Opção {opcao} não é válida.')
        return None

    subopcao = dicionario_opcao[opcao]
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao={subopcao}'
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        sub_sopa = BeautifulSoup(resposta.content, 'html.parser')
        tabela = sub_sopa.find('table', class_='tb_dados')
        if tabela:
            dados = []
            linhas = tabela.find_all('tr')
            produto_principal = None
            for linha in linhas[1:]:
                celulas = linha.find_all('td')
                if celulas:
                    if 'tb_item' in celulas[0].get('class', []):
                        produto_principal = celulas[0].get_text(strip=True)
                        quantidade = celulas[1].get_text(strip=True)
                        dados.append({'tabela': 'Processamento', 'produto': produto_principal, 'sub_produto': None, 'quantidade': quantidade, 'ano': ano, 'unidade_medida': 'kg'})
                    elif 'tb_subitem' in celulas[0].get('class', []):
                        sub_produto = celulas[0].get_text(strip=True)
                        quantidade = celulas[1].get_text(strip=True)
                        dados.append({'tabela': 'Processamento', 'produto': produto_principal, 'sub_produto': sub_produto, 'quantidade': quantidade, 'ano': ano, 'unidade_medida': 'kg'})
            df = pd.DataFrame(dados)
            
            # Remover valores nulos e selecionar apenas as colunas desejadas
            df = df.dropna(subset=['sub_produto'])
            df = df[['tabela', 'produto', 'sub_produto', 'quantidade', 'ano', 'unidade_medida']]
            
            return df
        else:
            print('Tabela não encontrada.')
            return None
    else:
        print('Falha ao fazer a solicitação HTTP para a página principal.')
        return None

# Remova a entrada do usuário via terminal
# if __name__ == "__main__":
#     opcao = input("Escolha uma opção (viniferas, americanas_hibridas, uvas_mesa, sem_classificacao): ").strip()
#     ano = int(input("Escolha o ano (1970-2022): "))

#     resultado = scrape_viti_processamento(ano, opcao)
#     if resultado is not None:
#         print(resultado)
#     else:
#         print("Nenhum dado encontrado.")
