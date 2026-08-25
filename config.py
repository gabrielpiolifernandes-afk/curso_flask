SECRET_KEY = 'Katatalzinho@312'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='NewMsql3000!',
        servidor='127.0.0.1',
        database='jogoteca'
    )