import hashlib

from Estruturas.GerenciadorTXT import GerenciadorTXT
from Estruturas.Nodes import Node
from Estruturas.ArvoreB import ArvoreB
from Estruturas.Controlador import Controlador

from Estruturas.RegistroIdiomas import RegistroIdiomas
from Estruturas.ControladorIdiomas import ControladorIdiomas

from Estruturas.RegistroUsuarios import RegistroUsuarios
from Estruturas.ControladorUsuarios import ControladorUsuarios

from Estruturas.RegistroLicoes import RegistroLicoes
from Estruturas.ControladorLicoes import ControladorLicoes

from Estruturas.RegistroExercicios import RegistroExercicios
from Estruturas.ControladorExercicios import ControladorExercicios

from Estruturas.RegistroExerciciosFeitos import RegistroExerciciosFeitos
from Estruturas.ControladorExerciciosFeitos import ControladorExerciciosFeitos

############################# MAIN ###############################
CI = ControladorIdiomas("idiomas.txt")
CL = ControladorLicoes("licoes.txt", CI)
CE = ControladorExercicios("exercicios.txt", CL)
CU = ControladorUsuarios("usuarios.txt", CI)
CEF = ControladorExerciciosFeitos("exercicios_feitos.txt", CU, CE)

CI.contruir_arvore_indices()
CL.contruir_arvore_indices()
CE.contruir_arvore_indices()
CU.contruir_arvore_indices()
CEF.contruir_arvore_indices()
