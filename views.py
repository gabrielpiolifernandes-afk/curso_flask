from flask import render_template,request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos,Usuarios
from helpers import recupera_imagem, deleta_arquivo, FormularioDeJogo, FormularioDeUsuario

import time 

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo_jogo', methods=['GET','POST'])
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioDeJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)

@app.route('/criar', methods=['POST'])
def criar():
    form = FormularioDeJogo(request.form)

    if form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

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
    uploads_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{uploads_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioDeJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogoteca = recupera_imagem(id)
    return render_template('editar.html', titulo='editando Jogo', id=id, capa_jogoteca=capa_jogoteca, form=form)

@app.route('/atualizar', methods=['POST'])
def atualizar():
    form = FormularioDeJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        uploads_path = app.config['UPLOAD_PATH']
        deleta_arquivo(jogo.id)
        timestamp = time.time()
        arquivo.save(f'{uploads_path}/capa{jogo.id}-{timestamp}.jpg')

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
    form = FormularioDeUsuario()
    if not proxima:
            proxima = url_for('index')
    return render_template('login.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioDeUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    if usuario: 
        if form.senha.data == usuario.senha:
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

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
