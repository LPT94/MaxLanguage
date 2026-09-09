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
ctrl_idiomas = ControladorIdiomas("idiomas.txt")
ctrl_licoes = ControladorLicoes("licoes.txt", ctrl_idiomas)
ctrl_exercicios = ControladorExercicios("exercicios.txt", ctrl_licoes)
ctrl_usuarios = ControladorUsuarios("usuarios.txt", ctrl_licoes)
ctrl_exe_feitos = ControladorExerciciosFeitos("exercicios_feitos.txt", ctrl_usuarios, ctrl_exercicios)


#LPT94 root

#LPT2 leo
#######################  FLASK  ###############################
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = "key"

@app.route("/", methods=["GET", "POST"])
def inicio():

    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]

        usuario = ctrl_usuarios.autenticar(login, senha)

        if usuario is None:
            session.pop("usuario_id", None)
            return "Login ou senha inválidos!"

        session["usuario_id"] = usuario.get_id()

        if usuario.get_tipo() == "0":
            return redirect("/admin")
        
        return redirect("/usuario")


    return render_template("login.html")

@app.route("/usuario")
def usuario():

    if "usuario_id" not in session:
        return "Para acessar esta página é necessário fazer login"

    usuario, node = ctrl_usuarios.get_registro(session["usuario_id"])

    if usuario.get_tipo() == "0":
        redirect("/admin")

    return render_template("usuario.html", usuario=usuario)


@app.route("/admin")
def admin():

    if "usuario_id" not in session:
        return "Area restrita, você precisa fazer login!"

    usuario, node = ctrl_usuarios.get_registro(session["usuario_id"])

    if usuario.get_tipo() != "0":
        return "Acesso negado!"

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

        sucesso = ctrl_usuarios.inserir_registro(novo_usuario)

        if sucesso:
            return redirect("/")

        return "Não foi possível criar a conta."

    lista_idiomas = ctrl_idiomas.listar_registros()

    
    return render_template("cadastro.html", idiomas=lista_idiomas)

if __name__ == "__main__":
    app.run(debug=True)

