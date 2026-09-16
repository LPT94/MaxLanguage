from flask import Blueprint, render_template, redirect, request, session
from context import ctrl_idiomas, ctrl_licoes, ctrl_usuarios
from Registers.RegistroIdiomas import RegistroIdiomas
from Utils.decorators import admin_required

idioma_bp = Blueprint("idioma", __name__, url_prefix="/admin/idiomas")

@idioma_bp.route("")
@admin_required
def idiomas():

    lista_idiomas = ctrl_idiomas.listar_registros()
    
    return render_template("idiomas.html", idiomas=lista_idiomas)

@idioma_bp.route("/novo", methods=["GET", "POST"])
@admin_required
def idioma_novo():

    if request.method == "POST":
        descricao = request.form["descricao"]

        id = ctrl_idiomas.get_proximo_id()
        novo_idioma = RegistroIdiomas(id, descricao)

        sucesso, mensagem = ctrl_idiomas.inserir_registro(novo_idioma)

        if sucesso:
            return redirect("/admin/idiomas")

        return render_template("erro.html", titulo="Não foi possível cadastrar o idioma", mensagem=mensagem, voltar="/admin/idiomas/novo")

    return render_template("novo_idioma.html")

@idioma_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar_idioma(id):

    idioma = ctrl_idiomas.get_registro(id)

    if idioma is None:
        return render_template("erro.html", titulo="Idioma não encontrado", mensagem="Id do idioma solicitado não encontrado", voltar="/admin/idiomas")

    if request.method == "POST":
        descricao = request.form["descricao"]

        idioma_editado = RegistroIdiomas(id, descricao)
        sucesso, mensagem = ctrl_idiomas.editar_registro(idioma_editado)

        if sucesso:
            return redirect("/admin/idiomas")

        return render_template("erro.html", titulo="Não foi possível editar idioma", mensagem=mensagem, voltar=f"/admin/idiomas/editar/{id}")

    return render_template("editar_idioma.html", idioma=idioma)

@idioma_bp.route("/excluir/<int:id>")
@admin_required
def excluir_idioma(id):

    sucesso, mensagem = ctrl_idiomas.del_registro(id, [ctrl_licoes.verifica_referencia(1, id), ctrl_usuarios.verifica_referencia(1,id)])

    if sucesso:
        return redirect("/admin/idiomas")

    return render_template("erro.html", titulo="Não foi possível deletar o idioma", mensagem=mensagem, voltar="/admin/idiomas")