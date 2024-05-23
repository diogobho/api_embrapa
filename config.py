SECRET_KEY = 'embrapa'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'fuMbhrInziYYPGAPxqLGdVTIUHCxDUac',
        servidor = 'viaduct.proxy.rlwy.net:30626',
        database = 'railway'
    )

SQLALCHEMY_TRACK_MODIFICATIONS = False