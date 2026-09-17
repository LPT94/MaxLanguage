import hashlib
from flask import Blueprint, session, render_template, redirect, request
from context import ctrl_idiomas, ctrl_usuarios
from Registers.RegistroUsuarios import RegistroUsuarios

autenticacao_bp = Blueprint("autenticacao", __name__, url_prefix="/")

@autenticacao_bp.route("", methods=["GET", "POST"])
def inicio():

    session.pop("usuario_id", None)

    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]

        usuario = ctrl_usuarios.autenticar(login, senha)

        if usuario is None:
            session.pop("usuario_id", None)
            return render_template("erro.html", titulo="Não foi possível realizar o login", mensagem="Login ou senha inválidos!", voltar="/" )

        session["usuario_id"] = usuario.get_id()

        if usuario.get_tipo() == "0":
            return redirect("/admin")
        
        return redirect("/usuario")


    return render_template("login.html")

@autenticacao_bp.route("/logout")
def logout():

    session.pop("usuario_id", None)
    return redirect("/")

@autenticacao_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":
        nome = request.form["nome"]
        login = request.form["login"]
        senha = request.form["senha"]
        cod_idioma = request.form["cod_idioma"]

        codigo = ctrl_usuarios.get_proximo_id()
        senha_hash = hashlib.sha256(senha.encode("utf-8")).hexdigest()

        novo_usuario = RegistroUsuarios(codigo, cod_idioma, nome, login, senha_hash, 1, 0, 1)

        sucesso, mensagem = ctrl_usuarios.inserir_registro(novo_usuario)

        if sucesso:
            return redirect("/")

        return render_template("erro.html", titulo="Não foi possível realizar o cadastro", mensagem=mensagem, voltar="/")

    lista_idiomas = ctrl_idiomas.listar_registros()

    return render_template("cadastro.html", idiomas=lista_idiomas)

