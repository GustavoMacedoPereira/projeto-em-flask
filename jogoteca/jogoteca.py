from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

jogo1= Jogo('Tetris', 'Puzzle', 'Atari')
jogo2= Jogo('God od war', 'Rack n slash', 'Ps2')
jogo3= Jogo('Mortal Kombat', 'Luta', 'Ps2')
lista = [jogo1, jogo2, jogo3]

app = Flask(__name__)
app.secret_key= 'alura'

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Bruno Divino', 'BD', 'lohomora')
usuario2 = Usuario('Camila Ferreira', 'Mila', 'paozinho')
usuario3 = Usuario('Gustavo Macedo', 'GM', 'help')

usuarios = {
            usuario1.nickname: usuario1,
            usuario2.nickname: usuario2,
            usuario3.nickname: usuario3
            }

@app.route('/')
def index():
    return render_template('index_lista.html', titulo='Jogos',jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('index_novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('index_login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário desconectado!')
    return redirect(url_for('index'))

app.run(debug=True ,host='0.0.0.0', port=8080)