from flask import Flask, flash, render_template,request, redirect, session, flash, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Super Mario', 'Plataforma', 'Nintendo')
jogo2 = Jogo('The Legend of Zelda', 'Ação/Aventura', 'Nintendo')
jogo3 = Jogo('God of War', 'Ação', 'PlayStation')   
    
lista = [jogo1, jogo2, jogo3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Lucas', 'lucas', '456')
usuario2 = Usuario('João', 'joao_mata_porco', '567')
usuario3 = Usuario('Maria', 'MD_12', '678')

usuarios = {usuario1.nickname: usuario1, usuario2.nickname: usuario2, usuario3.nickname: usuario3}

app = Flask(__name__)
app.secret_key = 'Katatalzinho@312'

@app.route('/')
def index():
    
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo_jogo', methods=['GET','POST'])
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form ['nome']
    categoria = request.form ['categoria']
    console = request.form ['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]  
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash('Bem vindo, {}'.format(session['usuario_logado']))
            proxima_pagina = request.form['proxima']
            return redirect('{}'.format(proxima_pagina))
    else:
        flash('Senha incorreta')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))

    
app.run(debug=True)
