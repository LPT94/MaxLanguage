from flask import Blueprint, render_template, redirect, request, session
from context import ctrl_exercicios, ctrl_licoes, ctrl_idiomas
from Registers.RegistroExercicios import RegistroExercicios
from Utils.decorators import admin_required

exercicio_bp = Blueprint("exercicio", __name__, url_prefix="/admin/exercicios")

@exercicio_bp.route("")
@admin_required
def exercicio():

    lista_exercicios = ctrl_exercicios.listar_registros()
    
    dados = []

    for exercicio in lista_exercicios:
        licao = ctrl_licoes.get_registro(exercicio.get_licao())
        idioma = ctrl_idiomas.get_registro(licao.get_cod_idioma())
        dados.append({"exercicio": exercicio.get_id(), "idioma": idioma.get_descricao(), "licao": licao.get_descricao(), 
                      "nivel": exercicio.get_nivel(), "descricao":exercicio.get_descricao(), "pontuacao": exercicio.get_pontuacao()})

        print(dados)
    return render_template("exercicios.html", dados=dados)

@exercicio_bp.route("/novo", methods=["GET", "POST"])
@admin_required
def exercicio_novo():

    licoes = ctrl_licoes.listar_registros()

    if request.method == "POST":
        id = ctrl_exercicios.get_proximo_id()
        cod_licao = request.form["cod_licao"]
        nivel = request.form["nivel"]
        descricao = request.form["descricao"]
        op_a = request.form["a"]
        op_b = request.form["b"]
        op_c = request.form["c"]
        op_d = request.form["d"]
        opcao_correta = request.form["opcao_correta"]
        pontuacao = request.form["pontuacao"]

        novo_registro = RegistroExercicios(id, cod_licao, nivel, descricao, op_a, op_b, 
                                           op_c, op_d, opcao_correta, pontuacao)

        sucesso, mensagem = ctrl_exercicios.inserir_registro(novo_registro)

        if sucesso:
            return redirect("/admin/exercicios")

        return render_template("erro.html", titulo="Não foi possível inserir registro.", mensagem=mensagem, voltar="/admin/exercicios/novo")

    return render_template("novo_exercicio.html", licoes=licoes)

@exercicio_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar_exercicio(id):

    exercicio = ctrl_exercicios.get_registro(id)
    licoes = ctrl_licoes.listar_registros()
    licao = ctrl_licoes.get_registro(exercicio.get_licao())

    if request.method == "POST":
        cod_licao = request.form["cod_licao"]
        nivel = request.form["nivel"]
        descricao = request.form["descricao"]
        op_a = request.form["a"]
        op_b = request.form["b"]
        op_c = request.form["c"]
        op_d = request.form["d"]
        opcao_correta = request.form["opcao_correta"]
        pontuacao = request.form["pontuacao"]

        registro_editado = RegistroExercicios(id, cod_licao, nivel, descricao, op_a, op_b, op_c, op_d,
                                              opcao_correta, pontuacao)

        sucesso, mensagem = ctrl_exercicios.editar_registro(registro_editado)

        if sucesso:
            return redirect("/admin/exercicios")

        return render_template("erro.html", titulo="Não foi possível editar o exercício", mensagem=mensagem, voltar=f"/admin/exercicios/editar/{id}")

    return render_template("editar_exercicio.html", licoes=licoes, actual=licao, exercicio=exercicio)



