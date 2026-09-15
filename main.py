
from flask import Flask, render_template, request, session, redirect
from context import ctrl_idiomas, ctrl_licoes, ctrl_usuarios, ctrl_exercicios, ctrl_exe_feitos

from Registers.RegistroIdiomas import RegistroIdiomas
from Registers.RegistroUsuarios import RegistroUsuarios
from Registers.RegistroLicoes import RegistroLicoes
from Registers.RegistroExercicios import RegistroExercicios
from Registers.RegistroExerciciosFeitos import RegistroExerciciosFeitos

from Routes.idioma_routes import idioma_bp
from Routes.autenticacao_routes import autenticacao_bp
from Routes.admin import admin_bp
from Routes.usuario import usuario_bp
from Routes.licao_routes import licao_bp


#######################  FLASK  ###############################

app = Flask(__name__)
app.secret_key = "key"
app.register_blueprint(idioma_bp)
app.register_blueprint(autenticacao_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(licao_bp)


    
if __name__ == "__main__":
    app.run(debug=True)

