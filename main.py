from Estruturas.GerenciadorTXT import GerenciadorTXT
from Estruturas.Nodes import Node
from Estruturas.ArvoreB import ArvoreB
from Estruturas.Controlador import Controlador
from Estruturas.RegistroExercicios import RegistroExercicios
from Estruturas.ControladorExercicios import ControladorExercicios


CL = Controlador("licoes.txt")
CE = ControladorExercicios("exercicios.txt", CL)

        

CL.contruir_arvore_indices()
CE.contruir_arvore_indices()


CE.mostrar_arvore("Width")

print(CE._gerenciador_txt.listar_offsets())
R = RegistroExercicios(17,2,3,"aa", "bb", "cc", "dd", "ee", 5, 2)

CE.inserir_registro(R)

CE.ordenar_arquivo()      


print(CE._gerenciador_txt.listar_offsets())