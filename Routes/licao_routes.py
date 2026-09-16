from flask import Blueprint, render_template, redirect, request, session
from context import ctrl_licoes, ctrl_idiomas, ctrl_exercicios
from Registers.RegistroLicoes import RegistroLicoes
from Utils.decorators import admin_required

licao_bp = Blueprint("licao", __name__, url_prefix="/admin/licoes")

@licao_bp.route("")
@admin_required
def licao():

    lista_licoes = ctrl_licoes.listar_registros()

    dados_licoes = []

    for licao in lista_licoes:
        idioma = ctrl_idiomas.get_registro(licao.get_cod_idioma()).get_descricao()
        dados_licoes.append({"licao": licao.get_id(), "idioma": idioma, "niveis": licao.get_total_niveis(), "descricao": licao.get_descricao()})

    return render_template("licoes.html", dados=dados_licoes)

    
@licao_bp.route("/novo", methods=["GET","POST"])
@admin_required
def licao_nova():

    idiomas = ctrl_idiomas.listar_registros()

    if request.method == "POST":
        id = ctrl_licoes.get_proximo_id()
        cod_idioma = request.form["cod_idioma"]
        total_niveis = request.form["total_niveis"]
        descricao = request.form["descricao"]

        nova_licao = RegistroLicoes(id, cod_idioma, total_niveis, descricao)

        sucesso, mensagem = ctrl_licoes.inserir_registro(nova_licao)
        if sucesso:
            return redirect("/admin/licoes")

        return render_template("erro.html", titulo="Não foi possível cadastrar a lição.", mensagem=mensagem, voltar="/admin/licoes/novo")

    return render_template("nova_licao.html", idiomas=idiomas)

@licao_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar_licao(id):

    licao = ctrl_licoes.get_registro(id)
    idiomas = ctrl_idiomas.listar_registros()

    if request.method == "POST":
        cod_idioma = request.form["cod_idioma"]
        total_niveis = request.form["total_niveis"]
        descricao = request.form["descricao"]

        novo_registro = RegistroLicoes(id, cod_idioma, total_niveis, descricao)

        sucesso, mensagem = ctrl_licoes.editar_registro(novo_registro, ctrl_exercicios)
        if sucesso:
            return redirect("/admin/licoes")

        return render_template("erro.html", titulo="Não foi possível editar lição", mensagem=mensagem, voltar=f"/admin/licoes/editar/{id}")

    return render_template("editar_licao.html", licao=licao, idiomas=idiomas)

@licao_bp.route("/excluir/<int:id>", methods=["GET"])
@admin_required
def excluir_licao(id):

    sucesso, mensagem = ctrl_licoes.del_registro(id, [ctrl_exercicios.verifica_referencia(1, id)])
    if sucesso:
        return redirect("/admin/licoes")
    
    return render_template("erro.html", titulo="Não foi possível deletar esta lição", mensagem=mensagem, voltar="/admin/licoes")