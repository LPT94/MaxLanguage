from Estruturas.GerenciadorTxt import GerenciadorTxt
from Estruturas.Nodes import Node
from Estruturas.ArvoreB import ArvoreB
from Estruturas.Controlador import Controlador
from Estruturas.RegistroExercicios import RegistroExercicios
from Estruturas.ControladorExercicios import ControladorExercicios

CL = Controlador("licoes.txt")
CE = ControladorExercicios("exercicios.txt")

CE.contruir_arvore_indices()

CE.ordenar_arquivo()


CE.mostrar_arvore()