import os

SECRET_KEY = 'sua chave geral'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario= 'seu usuario',
        senha='sua senha',
        servidor= 'seu ip',
        database='jogoteca'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath('__file__')) + '/uploads'