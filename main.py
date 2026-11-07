from flask import Flask, abort, redirect, render_template, request, url_for
from sqlalchemy import func, inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models.conexao import Base, engine
from models.tecnicos_model import Tecnicos
from models.usuarios_model import Usuarios
from models.chamados_model import Chamados

app = Flask(__name__)

Base.metadata.create_all(bind=engine)

with engine.begin() as conexao:
    colunas_usuario = {
        coluna["name"] for coluna in inspect(conexao).get_columns("usuarios")
    }
    if "senha" not in colunas_usuario:
        conexao.execute(
            text("ALTER TABLE usuarios ADD COLUMN senha VARCHAR(100)")
        )
    if engine.dialect.name == "sqlite":
        conexao.exec_driver_sql(
            """
            CREATE TRIGGER IF NOT EXISTS usuarios_nome_unico_insert
            BEFORE INSERT ON usuarios
            WHEN EXISTS (
                SELECT 1 FROM usuarios
                WHERE lower(trim(nome)) = lower(trim(NEW.nome))
            )
            BEGIN
                SELECT RAISE(ABORT, 'usuario_nome_duplicado');
            END
            """
        )
        conexao.exec_driver_sql(
            """
            CREATE TRIGGER IF NOT EXISTS usuarios_email_unico_insert
            BEFORE INSERT ON usuarios
            WHEN EXISTS (
                SELECT 1 FROM usuarios
                WHERE lower(trim(email)) = lower(trim(NEW.email))
            )
            BEGIN
                SELECT RAISE(ABORT, 'usuario_email_duplicado');
            END
            """
        )
        conexao.exec_driver_sql(
            """
            CREATE TRIGGER IF NOT EXISTS usuarios_nome_unico_update
            BEFORE UPDATE OF nome ON usuarios
            WHEN EXISTS (
                SELECT 1 FROM usuarios
                WHERE id != OLD.id
                  AND lower(trim(nome)) = lower(trim(NEW.nome))
            )
            BEGIN
                SELECT RAISE(ABORT, 'usuario_nome_duplicado');
            END
            """
        )
        conexao.exec_driver_sql(
            """
            CREATE TRIGGER IF NOT EXISTS usuarios_email_unico_update
            BEFORE UPDATE OF email ON usuarios
            WHEN EXISTS (
                SELECT 1 FROM usuarios
                WHERE id != OLD.id
                  AND lower(trim(email)) = lower(trim(NEW.email))
            )
            BEGIN
                SELECT RAISE(ABORT, 'usuario_email_duplicado');
            END
            """
        )

with engine.connect() as conexao:
    print("Banco em uso:", conexao.exec_driver_sql("PRAGMA database_list").fetchone()[2])

Session = sessionmaker(bind=engine)


def _usuario_ja_cadastrado(session, nome, email, usuario_id=None):
    consulta = session.query(Usuarios.id).filter(
        (func.lower(func.trim(Usuarios.nome)) == nome.lower())
        | (func.lower(func.trim(Usuarios.email)) == email.lower())
    )
    if usuario_id is not None:
        consulta = consulta.filter(Usuarios.id != usuario_id)
    return consulta.first() is not None


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identificador = request.form.get('login', '').strip()
        senha = request.form.get('senha', '')

        with Session() as session:
            usuario = (
                session.query(Usuarios)
                .filter(
                    (
                        func.lower(func.trim(Usuarios.nome))
                        == identificador.lower()
                    )
                    | (
                        func.lower(func.trim(Usuarios.email))
                        == identificador.lower()
                    )
                )
                .first()
            )
            credenciais_validas = (
                usuario is not None
                and usuario.senha is not None
                and usuario.senha == senha
            )

        if credenciais_validas:
            return redirect(url_for('home'))

        return render_template('login.html', usuario_invalido=True), 401

    return render_template('login.html', usuario_invalido=False)


@app.route('/home')
def home():
    with Session() as session:
        chamados = (
            session.query(Chamados)
            .order_by(Chamados.data_abertura.desc())
            .all()
        )

    total_chamados = len(chamados)
    total_fechados = sum(1 for chamado in chamados if chamado.status == 'Fechado')
    total_abertos = total_chamados - total_fechados

    contagem_status = {}
    for chamado in chamados:
        status = chamado.status or 'Sem status'
        contagem_status[status] = contagem_status.get(status, 0) + 1

    status_prioritarios = ['Aberto', 'Em andamento', 'Fechado']
    status_exibidos = status_prioritarios + sorted(
        status for status in contagem_status if status not in status_prioritarios
    )
    status_chart = [
        {
            'nome': status,
            'quantidade': contagem_status.get(status, 0),
            'percentual': round(
                contagem_status.get(status, 0) / total_chamados * 100,
                2,
            ) if total_chamados else 0,
        }
        for status in status_exibidos
    ]

    return render_template(
        'home.html',
        chamados=chamados,
        total_chamados=total_chamados,
        total_abertos=total_abertos,
        total_fechados=total_fechados,
        status_chart=status_chart,
    )


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/cadastro_chamado', methods=['GET', 'POST'])
def cadastro_chamado():

    if request.method == 'POST':

        titulo = request.form['titulo']
        descricao = request.form['descricao']
        status = request.form['status']
        prioridade = request.form['prioridade']
        categoria = request.form['categoria']
        id_usuario = request.form['id_usuario']
        responsavel_tecnico = request.form['responsavel_tecnico']

        data_abertura = datetime.now()
        data_fechamento = None

        chamado = Chamados(
            titulo,
            descricao,
            data_abertura,
            data_fechamento,
            status,
            prioridade,
            categoria,
            id_usuario,
            responsavel_tecnico
        )

        with Session() as session:
            session.add(chamado)
            session.commit()

        return redirect(url_for('chamado_cadastrado'))

    return render_template('cadastro_chamado.html')


@app.route('/chamado_cadastrado')
def chamado_cadastrado():
    return render_template('chamado_cadastrado.html')


@app.route('/cadastro_tecnico', methods=['GET', 'POST'])
def cadastro_tecnico():

    if request.method == 'POST':

        nome = request.form['nome']
        email = request.form['email']
        departamento = request.form['departamento']
        ramal = request.form['ramal']
        status = request.form['status']

        tecnico = Tecnicos(
            nome,
            email,
            departamento,
            ramal,
            status
        )

        session = Session()

        session.add(tecnico)
        session.commit()
        session.close()

        return 'Técnico cadastrado com sucesso!'

    return render_template('cadastro_tecnico.html')


@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():

    if request.method == 'POST':

        nome = request.form['nome'].strip()
        email = request.form['email'].strip().lower()
        senha = request.form['senha']
        departamento = request.form['departamento']
        ramal = request.form['ramal']
        status = request.form['status']

        mensagem_duplicado = (
            'Já existe um usuário cadastrado com esse nome ou e-mail. '
            'Use um nome de usuário e um e-mail diferentes.'
        )

        with Session() as session:
            if _usuario_ja_cadastrado(session, nome, email):
                return render_template(
                    'cadastro_usuario.html',
                    erro_cadastro=mensagem_duplicado,
                ), 409

        usuario = Usuarios(
            nome,
            email,
            senha,
            departamento,
            ramal,
            status
        )

        with Session() as session:
            session.add(usuario)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                if _usuario_ja_cadastrado(session, nome, email):
                    return render_template(
                        'cadastro_usuario.html',
                        erro_cadastro=mensagem_duplicado,
                    ), 409
                raise

        return redirect(url_for('usuario_cadastrado'))

    return render_template('cadastro_usuario.html')


@app.route('/usuario_cadastrado')
def usuario_cadastrado():
    return render_template('usuario_cadastrado.html')


@app.route('/listachamado')
def listachamado():
    with Session() as session:
        chamados = (
            session.query(Chamados)
            .order_by(Chamados.data_abertura.desc())
            .all()
        )

    return render_template('listar_chamados.html', chamados=chamados)


@app.route('/chamado/<int:chamado_id>/editar', methods=['GET', 'POST'])
def editar_chamado(chamado_id):
    with Session() as session:
        chamado = session.query(Chamados).filter_by(id=chamado_id).first()
        if chamado is None:
            abort(404)

        if request.method == 'POST':
            chamado.titulo = request.form['titulo']
            chamado.descricao = request.form['descricao']
            chamado.status = request.form['status']
            chamado.prioridade = request.form['prioridade']
            chamado.categoria = request.form['categoria']
            chamado.id_usuario = request.form['id_usuario']
            chamado.responsavel_tecnico = (
                request.form.get('responsavel_tecnico', '').strip() or None
            )
            session.commit()
            return redirect(url_for('listachamado'))

        dados_chamado = {
            'id': chamado.id,
            'titulo': chamado.titulo,
            'descricao': chamado.descricao,
            'status': chamado.status,
            'prioridade': chamado.prioridade,
            'categoria': chamado.categoria,
            'id_usuario': chamado.id_usuario,
            'responsavel_tecnico': chamado.responsavel_tecnico,
        }

    return render_template('editar_chamado.html', chamado=dados_chamado)


@app.route('/chamado/<int:chamado_id>/excluir', methods=['POST'])
def excluir_chamado(chamado_id):
    with Session() as session:
        chamado = session.query(Chamados).filter_by(id=chamado_id).first()
        if chamado is None:
            abort(404)

        session.delete(chamado)
        session.commit()

    return redirect(url_for('listachamado'))


@app.route('/listausuario')
def listausuario():
    with Session() as session:
        usuarios = (
            session.query(Usuarios)
            .order_by(Usuarios.nome.desc())
            .all()
        )

    return render_template('lista_usuarios.html', usuarios=usuarios)


@app.route('/usuario/<int:usuario_id>/editar', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    with Session() as session:
        usuario = session.query(Usuarios).filter_by(id=usuario_id).first()
        if usuario is None:
            abort(404)

        if request.method == 'POST':
            dados_usuario = {
                'id': usuario.id,
                'nome': request.form['nome'].strip(),
                'email': request.form['email'].strip().lower(),
                'departamento': request.form['departamento'],
                'ramal': request.form.get('ramal', '').strip() or None,
                'status': request.form['status'],
            }
            mensagem_duplicado = (
                'Já existe um usuário cadastrado com esse nome ou e-mail. '
                'Use um nome de usuário e um e-mail diferentes.'
            )
            if _usuario_ja_cadastrado(
                session,
                dados_usuario['nome'],
                dados_usuario['email'],
                usuario.id,
            ):
                return render_template(
                    'editar_usuario.html',
                    usuario=dados_usuario,
                    erro_cadastro=mensagem_duplicado,
                ), 409

            usuario.nome = dados_usuario['nome']
            usuario.email = dados_usuario['email']
            usuario.departamento = dados_usuario['departamento']
            usuario.ramal = dados_usuario['ramal']
            usuario.status = dados_usuario['status']

            nova_senha = request.form.get('senha', '').strip()
            if nova_senha:
                usuario.senha = nova_senha

            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                if _usuario_ja_cadastrado(
                    session,
                    dados_usuario['nome'],
                    dados_usuario['email'],
                    usuario.id,
                ):
                    return render_template(
                        'editar_usuario.html',
                        usuario=dados_usuario,
                        erro_cadastro=mensagem_duplicado,
                    ), 409
                raise
            return redirect(
                url_for('usuario_atualizado', usuario_id=usuario.id)
            )

        dados_usuario = {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'departamento': usuario.departamento,
            'ramal': usuario.ramal,
            'status': usuario.status,
        }

    return render_template('editar_usuario.html', usuario=dados_usuario)


@app.route('/usuario/<int:usuario_id>/atualizado')
def usuario_atualizado(usuario_id):
    with Session() as session:
        usuario = session.query(Usuarios).filter_by(id=usuario_id).first()
        if usuario is None:
            abort(404)

        dados_usuario = {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'departamento': usuario.departamento,
            'ramal': usuario.ramal,
            'status': usuario.status,
        }

    return render_template('usuario_atualizado.html', usuario=dados_usuario)


@app.route('/usuario/<int:usuario_id>/excluir', methods=['POST'])
def excluir_usuario(usuario_id):
    with Session() as session:
        usuario = session.query(Usuarios).filter_by(id=usuario_id).first()
        if usuario is None:
            abort(404)

        session.delete(usuario)
        session.commit()

    return redirect(url_for('listausuario'))


if __name__ == '__main__':
    app.run(debug=True)