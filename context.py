from Controllers.ControladorIdiomas import ControladorIdiomas
from Controllers.ControladorLicoes import ControladorLicoes
from Controllers.ControladorExercicios import ControladorExercicios
from Controllers.ControladorUsuarios import ControladorUsuarios
from Controllers.ControladorExerciciosFeitos import ControladorExerciciosFeitos

ctrl_idiomas = ControladorIdiomas("idiomas.txt")
ctrl_licoes = ControladorLicoes("licoes.txt", ctrl_idiomas)
ctrl_exercicios = ControladorExercicios("exercicios.txt", ctrl_licoes)
ctrl_usuarios = ControladorUsuarios("usuarios.txt", ctrl_idiomas)
ctrl_exe_feitos = ControladorExerciciosFeitos("exercicios_feitos.txt", ctrl_usuarios, ctrl_exercicios)