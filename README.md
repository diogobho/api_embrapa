# 🍇 Aplicação de Web Scraping de Vitivinicultura 🍷

## Visão Geral

Bem-vindo à Aplicação de Web Scraping de Vitivinicultura!

 Nossa aplicação faz a raspagem de dados do banco de dados Vitivinicultura (http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01) utilizando Python, Flask e várias outras ferramentas poderosas. Esta aplicação está implantada no Railway, documentada com Swagger e utiliza HTML e CSS para renderizar templates amigáveis ao usuário.

## Funcionalidades

### 🔒 Autenticação de Usuário
Nossa aplicação garante uma autenticação segura do usuário com proteção contra ataques CSRF e outras vulnerabilidades, proporcionando uma experiência segura e confiável.

### 📝 Registro de Novos Usuários
Os usuários podem se registrar facilmente na aplicação para acessar recursos exclusivos e personalizados.

### 📊 Raspagem de Dados
A aplicação coleta dados detalhados em várias áreas de acordo com o ano escolhido:
- **Produção**: Extrai dados de produção.
- **Processamento**: Coleta dados de processamento.
- **Comercialização**: Reúne dados de comercialização.
- **Importação**: Obtém dados de importação.
- **Exportação**: Recupera dados de exportação.

### 🌐 Implantação e Documentação
- **Implantação**: A aplicação é implantada de forma eficiente usando Railway.
- **Documentação**: A documentação completa da API está disponível via Swagger no [seguinte link](https://apiembrapa-production.up.railway.app/swagger).

## Tecnologias Utilizadas

- **Python**: Para scripts e processamento de dados.
- **Flask**: Como framework web para construir e executar a aplicação.
- **MySQL**: Para gerenciar e armazenar os dados de usuários.
- **Railway**: Para implantar a aplicação de maneira confiável e escalável.
- **Swagger**: Para fornecer uma documentação de API clara e amigável.
- **HTML & CSS**: Para projetar e renderizar templates web elegantes.

## Equipe

### Reryson Farinha
- **LinkedIn**: [Reryson Farinha](https://www.linkedin.com/in/reryson-farinha)
- **Email**: [rerysonfarinha1@gmail.com](mailto:rerysonfarinha1@gmail.com)

### Diogo Bortolozo
- **LinkedIn**: [Diogo Bortolozo](https://www.linkedin.com/in/diogo-bortolozo-6a0ba993)
- **Email**: [diogo_bho@hotmail.com](mailto:diogo_bho@hotmail.com)

## Primeiros Passos

### Pré-requisitos
Certifique-se de ter os seguintes itens instalados:
- Python 3.x
- Flask:
  - Flask-WTF
  - Flask-Bcrypt
  - Flask-Cors 
- MySQL
- Quaisquer outras dependências mencionadas no arquivo `requirements.txt`.

### Telas da aplicação:
- Tela de Login:
![TelaLogin](https://github.com/diogobho/api_embrapa/assets/119504068/75cd50da-9aac-4888-b00e-6c0bc65d65f5)

- Tela de Registro de usuários:
![Registro](https://github.com/diogobho/api_embrapa/assets/119504068/942ac765-5880-4ddf-baff-8f059c3e15b2)

- Tela de escolha de ano:
![ano](https://github.com/diogobho/api_embrapa/assets/119504068/9b385c2d-2720-4f16-a372-2d53c59bb3f4)

- Tela da renderização da tabela:
![table](https://github.com/diogobho/api_embrapa/assets/119504068/b5d7bc09-91fb-40eb-bc6f-04293ae60324)

#### Tela do banco de dados Vitivinicultura:
![image](https://github.com/diogobho/api_embrapa/assets/119504068/fd3232bd-5b1c-4915-98bd-bce95ee35862)





### Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/diogobho/api_embrapa.git
   cd api_embrapa
2. Instale os pacotes necessários:
   ```sh
    pip install -r requirements.txt
   ```

### Conclusão

Esperamos que você ache esta aplicação tão emocionante e útil quanto nós. Sinta-se à vontade para entrar em contato com qualquer membro da nossa equipe se tiver alguma dúvida ou sugestão. Feliz raspagem de dados! 🎉
