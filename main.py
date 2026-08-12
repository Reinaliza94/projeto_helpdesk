from flask import Flask, render_template

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

@app.route('/chamado')
def chamado():
 return render_template('cadastro_chamado.html')

@app.route('/tecnico')
def tecnico():
 return render_template('cadastro_tecnico.html')

#Inicia o servidor de desenvolvimento.
if __name__ == '__main__':
 app.run(debug=True)