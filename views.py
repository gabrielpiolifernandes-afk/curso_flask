from flask import render_template,request, redirect, session, flash, url_for
from jogoteca import app, db
from models import Jogos,Usuarios

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
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

    #serve para verificar se o jogo já existe no banco de dados
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já existente')
        return redirect(url_for('index'))
    
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    #esse comadando é um meio para guardar as imagens no proprio disco do computador, porem existe outro meio de guardar as imagens no proprio banco de dados, porem é mais complexo
    #e depende da situação aplicada, nesse caso não é necessario pois nao seram muitas imagens, porem a longo prazo provavelmente sera necessario um banco de dados so para imagens
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = Jogos.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='editando Jogo', jogo=jogo)

@app.route('/atualizar', methods=['POST'])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')

    if not proxima:
            proxima = url_for('index')

    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario: 
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash('Bem vindo, {}'.format(session['usuario_logado']))
            proxima_pagina = request.form['proxima']
            print('PROXIMA PÁGINA:', proxima_pagina)
            return redirect('{}'.format(proxima_pagina))
        else:
            flash('Senha incorreta')
            return redirect(url_for('login'))
    else:
        flash('Usuário não encontrado')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))