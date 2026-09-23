import hashlib
from flask import Blueprint, render_template, redirect, session, request
from context import ctrl_usuarios, ctrl_exe_feitos, ctrl_exercicios, ctrl_idiomas, ctrl_licoes
from Registers.RegistroUsuarios import RegistroUsuarios
from Registers.RegistroExerciciosFeitos import RegistroExerciciosFeitos
from Utils.decorators import user_required

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuario")


@usuario_bp.route("")
@user_required
def usuario():

    usuario = ctrl_usuarios.get_registro(session["usuario_id"])
    pontuacao = float(usuario.get_pontuacao())
    cod_idioma = usuario.get_cod_idioma()
    licoes = ctrl_licoes.listar_licoes_idioma(cod_idioma)

    dados = []

    for licao in licoes:
        nivel_abs = min(int(usuario.get_nivel_atual()), int(licao.get_total_niveis()))
        progresso = nivel_abs / int(licao.get_total_niveis()) * 100
        dados.append({"licao": licao.get_descricao(), "nivel_maximo": int(licao.get_total_niveis()), 
                      "nivel": nivel_abs, "progresso": progresso, "id": licao.get_id()})

    return render_template("usuario.html", usuario=usuario, dados_licoes=dados)


@usuario_bp.route("/licao/<int:id>")
@user_required
def usuario_licao(id):

    usuario = ctrl_usuarios.get_registro(session["usuario_id"])

    licao = ctrl_licoes.get_registro(id)
    if licao is None:
        return render_template("erro.html", titulo="Não foi possível acessar a lição!", mensagem="Lição solicitada não encontrada.", voltar="/usuario")

    if licao.get_cod_idioma() != usuario.get_cod_idioma():
        return render_template("erro.html", titulo="Acesso negado!", mensagem="Essa lição não pertence ao seu idioma.", voltar="/usuario")

    exercicios = ctrl_exercicios.registros_com_criterio({1: id})
    total_nivel = int(licao.get_total_niveis())
    nivel = int(usuario.get_nivel_atual())
    niveis = []

    for i in range(1, total_nivel+1):
        for exercicio in exercicios:
            if int(exercicio[2]) == i:
                niveis.append({"nivel": i, "desbloqueado": i <= nivel})
                break

   
    return render_template("usuario_licao.html", usuario=usuario, licao=licao, niveis=niveis)


@usuario_bp.route("/licao/<int:id>/nivel/<int:nivel>")
@user_required
def usuario_licao_exercicios(id, nivel):
    usuario = ctrl_usuarios.get_registro(session["usuario_id"])
    
    licao = ctrl_licoes.get_registro(id)
    if licao is None:
        return render_template("erro.html", titulo="Não foi possível acessar a lição!", mensagem="Lição solicitada não encontrada.", voltar="/usuario")

    if licao.get_cod_idioma() != usuario.get_cod_idioma():
        return render_template("erro.html", titulo="Acesso negado!", mensagem="Essa lição não pertence ao seu idioma.", voltar="/usuario")

    if int(nivel) < 1 or int(nivel) > int(licao.get_total_niveis()):
        return render_template("erro.html", titulo="Nivel inexistente!", mensagem="O nível solicitado não existe na lição.", 
                               voltar=f"/usuario/licao/{id}")

    nivel_usuario = usuario.get_nivel_atual()

    if int(nivel) > int(nivel_usuario):
        return render_template("erro.html", titulo="Acesso negado!", mensagem="Você não tem nível suficiente para acessar estes exercícios", 
                               voltar=f"/usuario/licao/{id}")

    dados_exercicios = ctrl_exercicios.registros_com_criterio({1:id, 2: nivel})
    lista_exercicios = []

    for dado in dados_exercicios:
        exe_feito = ctrl_exe_feitos.get_registro(int(usuario.get_id())*10000+int(dado[0]))
        lista_exercicios.append({"exercicio": ctrl_exercicios.get_registro(dado[0]),
                                 "feito": exe_feito})


    return render_template("usuario_licao_nivel.html", licao=licao, usuario=usuario, dados_exercicios=lista_exercicios, nivel=nivel)


@usuario_bp.route("/licao/<int:id>/nivel/<int:nivel>/exercicio/<int:exercicio_id>", methods=["GET", "POST"])
@user_required
def usuario_exercicio(id, nivel, exercicio_id):

    usuario = ctrl_usuarios.get_registro(session["usuario_id"])
        
    licao = ctrl_licoes.get_registro(id)
    if licao is None:
        return render_template("erro.html", titulo="Não foi possível acessar a lição!", mensagem="Lição solicitada não encontrada.", voltar="/usuario")

    if licao.get_cod_idioma() != usuario.get_cod_idioma():
        return render_template("erro.html", titulo="Acesso negado!", mensagem="Essa lição não pertence ao seu idioma.", voltar="/usuario")

    if int(nivel) < 1 or int(nivel) > int(licao.get_total_niveis()):
        return render_template("erro.html", titulo="Nivel inexistente!", mensagem="O nível solicitado não existe na lição.", 
                                voltar=f"/usuario/licao/{id}")
    
    nivel_usuario = usuario.get_nivel_atual()

    if int(nivel) > int(nivel_usuario):
        return render_template("erro.html", titulo="Acesso negado!", mensagem="Você não tem nível suficiente para acessar este exercício.", 
                                voltar=f"/usuario/licao/{id}")

    exercicio = ctrl_exercicios.get_registro(exercicio_id)

    if exercicio is None:
        return render_template("erro.html", titulo="Exercício não encontrado", mensagem="O exercício que você selecionou não foi encontrado.",
                               voltar=f"/licao/{id}/nivel/{nivel}")

    if int(exercicio.get_licao()) != id:
        return render_template("erro.html", titulo="Exercício inválido", mensagem="Este exercício não pertence à lição informada.",
                               voltar=f"/licao/{id}/nivel/{nivel}")

    if int(exercicio.get_nivel()) != nivel:
        return render_template("erro.html", titulo="Exercício inválido", mensagem="Este exercício não pertence ao nível informado.",
            voltar=f"/usuario/licao/{id}/nivel/{nivel}")

    if request.method == "GET":
        return render_template("usuario_exercicio.html", usuario=usuario, licao=licao, nivel=nivel, exercicio=exercicio)

    resposta = request.form.get("resposta")

    if resposta is None:
        return render_template("erro.html", titulo="Resposta inválida", mensagem="Nenhuma alternativa foi selecionada.",
            voltar=f"/usuario/licao/{id}/nivel/{nivel}/exercicio/{nivel}")

    if resposta == exercicio.get_op_correta():

        registro = ctrl_exe_feitos.get_registro(int(usuario.get_id())*10000+int(exercicio_id))
        if not registro:
            sucesso, mensagem = ctrl_exe_feitos.inserir_registro(RegistroExerciciosFeitos(usuario.get_id(), exercicio_id))
            if not sucesso:
                return render_template("erro.html", titulo="Não foi possível salvar o exercício realizado.", mensagem=mensagem,
                                        voltar=f"/usuario/licao/{id}/nivel/{nivel}/exercicio/{exercicio_id}")

        mensagem = "Parabens, você acertou!"

        if float(usuario.get_pontuacao()) < float(nivel)*100:
            pontuacao_antiga =  float(usuario.get_pontuacao())
            nova_pontuacao = float(exercicio.get_pontuacao()) + pontuacao_antiga
            
            nivel_atual = int(usuario.get_nivel_atual())
            if nova_pontuacao >= float(nivel_atual)*100:
                novo_nivel =  nivel_atual + 1
                usuario.set_nivel_atual(novo_nivel)

            usuario.set_pontuacao(nova_pontuacao)
            
            sucesso, mensagem = ctrl_usuarios.editar_registro(usuario)
            if not sucesso:
                return render_template("erro.html", titulo="Não foi possível salvar resposta", mensagem=mensagem,
                voltar=f"/usuario/licao/{id}/nivel/{nivel}/exercicio/{exercicio_id}")


            mensagem = f"Parabens você acertou! Ganhou +{exercicio.get_pontuacao()} pontos."

        return render_template("acerto.html", mensagem=mensagem, voltar=f"/usuario/licao/{id}/nivel/{nivel}")

    pontuacao_antiga = float(usuario.get_pontuacao())
    pontos = float(exercicio.get_pontuacao())
    perda = 0.1 * pontos
    nova_pontuacao = pontuacao_antiga - perda

    if nova_pontuacao > 0:
        usuario.set_pontuacao(nova_pontuacao)
        sucesso, mensagem = ctrl_usuarios.editar_registro(usuario)
        if not sucesso:
            return render_template("erro.html", titulo="Não foi possível salvar resposta", mensagem=mensagem,
            voltar=f"/usuario/licao/{id}/nivel/{nivel}")

        mensagem=f"Resposta incorreta. Você perdeu {perda:.2f} pontos."
    else:
        mensagem="Resposta incorreta"

    return render_template(
        "erro.html",
        titulo="Resposta incorreta",
        mensagem=mensagem,
        voltar=f"/usuario/licao/{id}/nivel/{nivel}"
    )

@usuario_bp.route("/meu_perfil/<int:id>", methods=["GET", "POST"])
@user_required
def usuario_perfil(id):

    usuario = ctrl_usuarios.get_registro(session["usuario_id"])
    if int(usuario.get_id()) != id:
        return render_template("erro.html", titulo="Acesso Negado.", mensagem="Você não está permitido acessar esta página.", voltar="/usuario")

    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]

        if senha:
            senha_hash = hashlib.sha256(senha.encode("utf-8")).hexdigest()

            usuario.set_login(login)
            usuario.set_senha(senha_hash)

            sucesso, mensagem = ctrl_usuarios.editar_registro(usuario)
            if not sucesso:
                return render_template("erro.html", titulo="Erro ao alterar login/senha", mensagem=mensagem, voltar=f"/usuario/meu_perfil/{id}")

        return redirect("/usuario")

    return render_template("usuario_perfil.html", usuario=usuario)


@usuario_bp.route("/ranking")
@user_required
def usuario_ranking():

    ranking = ctrl_usuarios.listar_ranking()
    usuario = ctrl_usuarios.get_registro(session["usuario_id"])

    return render_template("ranking.html", usuario=usuario, usuarios=ranking)


@usuario_bp.route("/certificado")
@user_required
def usuario_certificado():

    usuario = ctrl_usuarios.get_registro(session["usuario_id"])
    idioma = ctrl_idiomas.get_registro(usuario.get_cod_idioma())
    lista_licoes = ctrl_licoes.registros_com_criterio({1: usuario.get_cod_idioma()})
    lista_codigos = []
    for licao in lista_licoes:
        lista_codigos.append(licao[0])

    nivel_maximo = ctrl_exercicios.maior_nivel(lista_codigos)
    if nivel_maximo < int(usuario.get_nivel_atual()):
        return render_template("certificado.html", usuario=usuario, idioma=idioma)
    
    return render_template("erro.html", titulo="Acesso negado!", 
                           mensagem="Você ainda não atingiu o nível suficiente para obter o certificado.", 
                           voltar="/usuario")


