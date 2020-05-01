from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Funcionario
from dao import FuncionarioDao, UsuarioDao
import time
from cadastro import db, app
from helpers import deleta_arquivo, recupera_imagem

funcionario_dao = FuncionarioDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    lista = funcionario_dao.listar()
    return render_template('lista.html', titulo='Funcionários', funcionarios=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Funcionário')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    cargo = request.form['cargo']
    setor = request.form['setor']
    funcionario = Funcionario(nome, cargo, setor)
    funcionario = funcionario_dao.salvar(funcionario)

    arquivo = request.files['arquivo']
    uploard_path = app.config['UPLOARD_PATH']
    timestamp = time.time()
    arquivo.save(f'{uploard_path}/foto{funcionario.id}-{timestamp}.jpg')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    funcioanrio = funcionario_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Funcionário', funcionario=funcioanrio
                           ,capa_foto=nome_imagem or 'foto_padrao.jpg')



@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    cargo = request.form['cargo']
    setor = request.form['setor']
    funcionario = Funcionario(nome, cargo, setor, id=request.form['id'])

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(funcionario.id)
    arquivo.save(f'{upload_path}/foto{funcionario.id}-{timestamp}.jpg')
    funcionario_dao.salvar(funcionario)
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    funcionario_dao.deletar(id)
    flash('Funcionário removido com sucesso!')
    return redirect(url_for('index'))



@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
       if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhun usuário logado!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

