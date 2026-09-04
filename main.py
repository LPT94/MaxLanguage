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


############################# MAIN ###############################
CI = ControladorIdiomas("idiomas.txt")
CL = ControladorLicoes("licoes.txt", CI)
CE = ControladorExercicios("exercicios.txt", CL)

CI.contruir_arvore_indices()
CL.contruir_arvore_indices()
CE.contruir_arvore_indices()

CE.mostrar_arvore()

RE = RegistroExercicios(3, 3, 3, "DESC", "A", "B", "C", "D", 6, 10)

CE.inserir_registro(RE)