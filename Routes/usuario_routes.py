from flask import Blueprint, render_template, redirect, session, request
from context import ctrl_usuarios, ctrl_idiomas, ctrl_exe_feitos
from Registers.RegistroUsuarios import RegistroUsuarios
from Utils.decorators import admin_required

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/admin/usuarios")

@usuarios_bp.route("")
@admin_required
def usuario():

    lista_usuarios = ctrl_usuarios.listar_registros()
    usuarios = []

    for usuario in lista_usuarios:
        codigo = usuario.get_id()
        idioma = ctrl_idiomas.get_registro(usuario.get_cod_idioma())
        nome = usuario.get_nome()
        login = usuario.get_login()
        nivel_atual = usuario.get_nivel_atual()
        pontuacao = usuario.get_pontuacao()

        if usuario.get_tipo() == '0':
            tipo = "Administrador"
        else:
            tipo = "Usuário"
        
        usuarios.append({'id': codigo, 'idioma': idioma.get_descricao(), 'nome': nome, 'login': login, 
                         'nivel_atual':nivel_atual, 'pontuacao':pontuacao, 'tipo':tipo})


    return render_template("usuarios.html", usuarios=usuarios)

@usuarios_bp.route("/novo", methods=["GET", "POST"])
@admin_required
def usuario_novo():

    idiomas = ctrl_idiomas.listar_registros()

    if request.method == "POST":
        codigo = ctrl_usuarios.get_proximo_id()
        cod_idioma = request.form["cod_idioma"]
        nome = request.form["nome"]
        login = request.form["login"]
        senha = request.form["senha"]
        nivel_atual = request.form["nivel_atual"]
        pontuacao = request.form["pontuacao"]
        tipo = request.form["tipo"]

        novo_usuario = RegistroUsuarios(codigo, cod_idioma, nome, login, senha, nivel_atual, pontuacao, tipo)

        sucesso, mensagem = ctrl_usuarios.inserir_registro(novo_usuario)

        if sucesso:
            return redirect("/admin/usuarios")

        return render_template("erro.html", titulo="Não foi possível cadastrar o usuário.", mensagem=mensagem, voltar="/admin/usuarios/novo")

    return render_template("novo_usuario.html", idiomas=idiomas)

@usuarios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar_usuario(id):

    usuario = ctrl_usuarios.get_registro(id)
    idiomas = ctrl_usuarios.listar_registros()

    if request.method == "POST":
        cod_idioma = request.form["cod_idioma"]
        nome = request.form["nome"]
        login = request.form["login"]
        senha = request.form["senha"]
        nivel_atual = request.form["nivel_atual"]
        pontuacao = request.form["pontuacao"]
        tipo = request.form["tipo"]

        usuario_editado = RegistroUsuarios(id, cod_idioma, nome, login, senha, nivel_atual, pontuacao, tipo)

        sucesso, mensagem = ctrl_usuarios.editar_registro(usuario_editado)
        if sucesso:
            return redirect("/admin/usuarios")

        return render_template("erro.html", titulo="Não foi possível editar o usuário", mensagem=mensagem, valor=f"admin/usuarios/editar/{id}")

    return render_template("editar_usuario.html", idiomas=idiomas, usuario=usuario)
        

