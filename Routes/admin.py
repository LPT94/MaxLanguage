from flask import Blueprint, render_template, redirect, session
from context import ctrl_usuarios

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("")
def admin():

    if "usuario_id" not in session:
        return render_template("erro.html", titulo="Area restrita", mensagem="Área restrita, você precisa fazer login!", voltar="/")

    usuario = ctrl_usuarios.get_registro(session["usuario_id"])

    if usuario.get_tipo() != "0":
        return redirect("/usuario")

    return render_template("admin.html", usuario=usuario)

