from flask import Blueprint, render_template, redirect, request, session
from context import ctrl_licoes, ctrl_idiomas, ctrl_usuarios, ctrl_exercicios
from Registers.RegistroLicoes import RegistroLicoes

licao_bp = Blueprint("licao", __name__, url_prefix="/admin/licoes")

@licao_bp.route("")
def licao():

    if "usuario_id" not in session:
        return render_template("erro.html", titulo="Área restrita", mensagem="Área restrita, você precisa fazer login!", voltar="/")

    usuario = ctrl_usuarios.get_registro(session["usuario_id"])

    if usuario.get_tipo() != "0":
        return redirect("/usuario")

    lista_licoes = ctrl_licoes.listar_registros()

    dados_licoes = []

    for licao in lista_licoes:
        idioma = ctrl_idiomas.get_registro(licao.get_cod_idioma()).get_descricao()
        dados_licoes.append({"licao": licao.get_id(), "idioma": idioma, "niveis": licao.get_total_niveis()})

    return render_template("licoes.html", usuario=usuario, dados=dados_licoes)

    
@licao_bp.route("/novo", methods=["GET","POST"])
def licao_nova():

    if "usuario_id" not in session:
        return render_template("erro.html", titulo="Área restrita", mensagem="Área restrita, você precisa fazer login!", voltar="/")
    
    usuario = ctrl_usuarios.get_registro(session["usuario_id"])

    if usuario.get_tipo() != "0":
        return redirect("/usuario")

    idiomas = ctrl_idiomas.listar_registros()

    if request.method == "POST":
        id = ctrl_licoes.get_proximo_id()
        cod_idioma = request.form["cod_idioma"]
        total_niveis = request.form["total_niveis"]

        nova_licao = RegistroLicoes(id, cod_idioma, total_niveis)

        print("id: ", id, " cod_idioma: ", cod_idioma, " total_niveis: ", total_niveis)
        sucesso, mensagem = ctrl_licoes.inserir_registro(nova_licao)
        if sucesso:
            return redirect("/admin/licoes")

        render_template("erro.html", titulo="Não foi possível cadastrar a lição.", mensagem=mensagem, voltar="/admin/licoes/novo")

    return render_template("nova_licao.html", idiomas=idiomas)

@licao_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_licao(id):

    if "usuario_id" not in session:
        return render_template("erro.html", titulo="Área restrita", mensagem="Área restrita, você precisa fazer login!", voltar="/")

    usuario = ctrl_usuarios.get_registro(session["usuario_id"])

    if usuario.get_tipo() != "0":
        return redirect("/usuario")

    licao = ctrl_licoes.get_registro(id)
    idiomas = ctrl_idiomas.listar_registros()

    if request.method == "POST":
        cod_idioma = request.form["cod_idioma"]
        total_niveis = request.form["total_niveis"]

        novo_registro = RegistroLicoes(id, cod_idioma, total_niveis)

        sucesso, mensagem = ctrl_licoes.editar_registro(novo_registro, ctrl_exercicios)

        if sucesso:
            return redirect("/admin/licoes")

        return render_template("erro.html", titulo="Não foi possível editar lição", mensagem=mensagem, voltar=f"/admin/licoes/editar/{id}")

    return render_template("editar_licao.html", licao=licao, idiomas=idiomas, usuario=usuario)

