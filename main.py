from flask import Flask, render_template, request, redirect, url_for

from models.usuarios_model import *
from models.chamados_model import *
from models.conexao import *
from datetime import datetime

app = Flask(__name__)

# Criação de uma instância do Flask
app = Flask(__name__)

# Definição de uma rota
@app.route('/')
def login():
 return render_template('login.html')

@app.route('/home')
def home():
 return render_template('home.html')

@app.route('/menu')
def menu():
 return render_template('menu.html')    

@app.route('/cadastro_chamado', methods=["GET", "POST"])
def cadastro_chamado():

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        status = request.form["status"]
        prioridade = request.form["prioridade"]
        categoria = request.form["categoria"]
        id_usuario = request.form["id_usuario"]
        responsavel_tecnico = request.form["responsavel_tecnico"]

        data_abertura = datetime.now()
        data_fechamento = None

        chamado = Chamados(titulo, descricao, data_abertura, data_fechamento, status, prioridade, categoria, id_usuario, responsavel_tecnico)
        
        session = Session()

        session.add(chamado)
        session.commit()

        session.close()

        return "Chamado cadastrado com sucesso!"

    return render_template("cadastro_chamado.html")


@app.route("/cadastro_tecnico")
def cadastro_tecnico():
    return render_template("cadastro_tecnico.html")


@app.route("/cadastro_usuario", methods=["GET", "POST"])
def cadastro_usuario():

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        departamento = request.form["departamento"]
        ramal = request.form["ramal"]
        status = request.form["status"]

        usuario = Usuarios(nome, email, departamento, ramal, status)

        session = Session()
        session.add(usuario)
        session.commit()
        session.close()

        return "Usuário cadastrado com sucesso!"

    return render_template("cadastro_usuario.html")

@app.route('/listachamado')
def listachamado():
 return render_template('listar_chamados.html')

#Inicia o servidor de desenvolvimento.
if __name__ == '__main__':
 app.run(debug=True)