import os 
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField
from jogoteca import app

class FormularioDeJogo(FlaskForm):
    nome = StringField('Nome do Jogo',{validators.DataRequired(),validators.Length(min=1,max=50)})
    categoria = StringField('Categoria do Jogo',{validators.DataRequired(),validators.Length(min=1,max=40)})
    console = StringField('Console do Jogo',{validators.DataRequired(),validators.Length(min=1,max=20)})
    salvar = SubmitField('Salvar')

class FormularioDeUsuario(FlaskForm):
    nickname = StringField('Nickname do Usuário',{validators.DataRequired(),validators.Length(min=1,max=8)})
    senha = PasswordField('Senha do Usuário',{validators.DataRequired(),validators.Length(min=1,max=100)})
    login = SubmitField('Login')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_jogoteca.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_jogoteca.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))

