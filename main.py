import hashlib

from Registers.RegistroIdiomas import RegistroIdiomas
from Controllers.ControladorIdiomas import ControladorIdiomas

from Registers.RegistroUsuarios import RegistroUsuarios
from Controllers.ControladorUsuarios import ControladorUsuarios

from Registers.RegistroLicoes import RegistroLicoes
from Controllers.ControladorLicoes import ControladorLicoes

from Registers.RegistroExercicios import RegistroExercicios
from Controllers.ControladorExercicios import ControladorExercicios

from Registers.RegistroExerciciosFeitos import RegistroExerciciosFeitos
from Controllers.ControladorExerciciosFeitos import ControladorExerciciosFeitos


############################# MAIN ###############################
ctrl_idiomas = ControladorIdiomas("idiomas.txt", )
ctrl_licoes = ControladorLicoes("licoes.txt", ctrl_idiomas)
ctrl_exercicios = ControladorExercicios("exercicios.txt", ctrl_licoes)
ctrl_usuarios = ControladorUsuarios("usuarios.txt", ctrl_idiomas)
ctrl_exe_feitos = ControladorExerciciosFeitos("exercicios_feitos.txt", ctrl_usuarios, ctrl_exercicios)


#LPT94 root

#LPT2 leo
#######################  FLASK  ###############################
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = "key"

@app.route("/", methods=["GET", "POST"])
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

@app.route("/logout")
def logout():

    session.pop("usuario_id", None)
    return redirect("/")


@app.route("/usuario")
def usuario():

    if "usuario_id" not in session:
        return "Para acessar esta página é necessário fazer login"

    usuario, node = ctrl_usuarios.get_registro(session["usuario_id"])

    if usuario.get_tipo() == "0":
       return redirect("/admin")

    if usuario.get_tipo() != "1":
        return redirect("/")
    
    return render_template("usuario.html", usuario=usuario)


@app.route("/admin")
def admin():

    if "usuario_id" not in session:
        return "Area restrita, você precisa fazer login!"

    usuario, node = ctrl_usuarios.get_registro(session["usuario_id"])

    if usuario.get_tipo() != "0":
        return redirect("/usuario")

    return render_template("admin.html", usuario=usuario)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":
        nome = request.form["nome"]
        login = request.form["login"]
        senha = request.form["senha"]
        cod_idioma = request.form["cod_idioma"]

        id = ctrl_usuarios.get_proximo_id()
        senha_hash = hashlib.sha256(senha.encode("utf-8")).hexdigest()

        novo_usuario = RegistroUsuarios(id, cod_idioma, nome, login, senha_hash, 1, 0, 1)

        sucesso, mensagem = ctrl_usuarios.inserir_registro(novo_usuario)

        if sucesso:
            return redirect("/")

        return render_template("erro.html", titulo="Não foi possível realizar o cadastro", mensagem=mensagem, voltar="/")

    lista_idiomas = ctrl_idiomas.listar_registros()

    return render_template("cadastro.html", idiomas=lista_idiomas)

@app.route("/admin/idiomas")
def idiomas():

    if "usuario_id" not in session:
            return "Area restrita, você precisa fazer login!"
    
    usuario, node = ctrl_usuarios.get_registro(session["usuario_id"])
    
    if usuario.get_tipo() != "0":
        return redirect("/usuario")

    lista_idiomas = ctrl_idiomas.listar_registros()

    return render_template("idiomas.html", usuario=usuario, idiomas=lista_idiomas)

@app.route("/admin/idiomas/novo", methods=["GET", "POST"])
def idioma_novo():

    if "usuario_id" not in session:
        return "Area restrita, você precisa fazer login!"
        
    usuario, node = ctrl_usuarios.get_registro(session["usuario_id"])
    
    if usuario.get_tipo() != "0":
        return redirect("/usuario")

    if request.method == "POST":
        descricao = request.form["descricao"]

        id = ctrl_idiomas.get_proximo_id()
        novo_idioma = RegistroIdiomas(id, descricao)

        sucesso, mensagem = ctrl_idiomas.inserir_registro(novo_idioma)

        if sucesso:
            return redirect("/admin/idiomas")

        return render_template("erro.html", titulo="Não foi possível cadastrar o idioma", mensagem=mensagem, voltar="/admin/idiomas/novo")

    return render_template("novo_idioma.html", usuario=usuario)

@app.route("/admin/idiomas/editar/<int:id>", methods=["GET", "POST"])
def editar_idioma(id):
    if "usuario_id" not in session:
        return redirect("/")

    usuario, node = ctrl_usuarios.get_registro(session["usuario_id"])

    if usuario.get_tipo() != "0":
        return "Acesso Negado"

    idioma, node = ctrl_idiomas.get_registro(id)

    if idioma is None:
        return render_template("erro.html", titulo="Idioma não encontrado", mensagem="Id do idioma solicitado não encontrado", voltar="/admin/idiomas")

    if request.method == "POST":
        descricao = request.form["descricao"]

        idioma_editado = RegistroIdiomas(id, descricao)
        sucesso, mensagem = ctrl_idiomas.editar_registro(idioma_editado)

        if sucesso:
            return redirect("/admin/idiomas")

        return render_template("erro.html", titulo="Não foi possível editar idioma", mensagem=mensagem, voltar=f"/admin/idiomas/editar/{id}")

    return render_template("editar_idioma.html", usuario=usuario, idioma=idioma)

@app.route("/admin/idiomas/excluir/<int:id>")
def excluir_idioma(id):
    if "usuario_id" not in session:
        return redirect("/")

    usuario, node = ctrl_usuarios.get_registro(session["usuario_id"])

    if usuario.get_tipo() != "0":  
        return "Acesso Negado"

    idioma, node = ctrl_idiomas.get_registro(id)

    if idioma is None:
        return render_template("erro.html", titulo="Idioma não encontrado", mensagem="Id do idioma solicitado não encontrado", voltar="/admin/idiomas")

    sucesso, mensagem = ctrl_idiomas.del_registro(id, [ctrl_licoes.verifica_referencia(1, id), ctrl_usuarios.verifica_referencia(1,id)])

    if sucesso:
        return redirect("/admin/idiomas")

    print(ctrl_idiomas.mostrar_arvore())
    return render_template("erro.html", titulo="Não foi possível deletar o idioma", mensagem=mensagem, voltar="/admin/idiomas")

    
if __name__ == "__main__":
    app.run(debug=True)

