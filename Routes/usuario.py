from flask import Blueprint, render_template, redirect, session
from context import ctrl_usuarios

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuario")

@usuario_bp.route("")
def usuario():

    if "usuario_id" not in session:
        return render_template("erro.html",titulo="Acesso negado!", mensagem="Para acessar esta página é necessário fazer login", voltar="/")

    usuario = ctrl_usuarios.get_registro(session["usuario_id"])

    if usuario.get_tipo() == "0":
       return redirect("/admin")

    if usuario.get_tipo() != "1":
        return redirect("/")
    
    return render_template("usuario.html", usuario=usuario)