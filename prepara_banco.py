import mysql.connector
from mysql.connector import errorcode
from urllib.parse import urlparse
from flask_bcrypt import generate_password_hash

# Credenciais fornecidas pelo Railway
MYSQL_URL = "mysql://root:fuMbhrInziYYPGAPxqLGdVTIUHCxDUac@viaduct.proxy.rlwy.net:30626/railway"

# Parse the MYSQL_URL to extract the connection details
url = urlparse(MYSQL_URL)
host = url.hostname
port = url.port
user = url.username
password = url.password
database = url.path[1:]  # remove the leading '/'

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)
    exit(1)

# Criando tabela de usuários
TABLES = {}
TABLES['Usuarios'] = ('''
      CREATE TABLE IF NOT EXISTS `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

# Executando a criação da tabela
for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

# Inserindo usuários
usuario_sql = 'INSERT IGNORE INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
    ("Bruno Divino", "BD", generate_password_hash("alohomora").decode('utf-8') ),
    ("Camila Ferreira", "Mila", generate_password_hash("paozinho").decode('utf-8')),
    ("Guilherme Louro", "Cake", generate_password_hash("python_eh_vida").decode('utf-8')),
    ("Diogo", "Didico", generate_password_hash("teste").decode('utf-8')),
    ("Reryson", "Re", generate_password_hash("teste").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

# Selecionando e exibindo os usuários
cursor.execute('SELECT * FROM usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user)

# Commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
