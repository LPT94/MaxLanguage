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

