from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'leandro'

class Funcionario:
    def __init__(self, nome, cargo, setor,):
        self.nome = nome
        self.cargo = cargo
        self.setor = setor

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

usuario1 = Usuario('Leandro', 'Leandro H', '123')
usuario2 = Usuario('Karine', 'Karine M', '123')

usuarios = {usuario1.id: usuario1, usuario2.id: usuario2 }

funcionario1 = Funcionario('Leandro', 'Programador', 'Desenvolvimanto')
funcionario2 = Funcionario('Karine', 'Diretora', 'Adm')
funcionario3 = Funcionario('Leda', 'Diretora', 'Adm')
lista = [funcionario1, funcionario2, funcionario3]

@app.route('/')
def index():
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
    lista.append(funcionario)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
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


app.run(debug=True)