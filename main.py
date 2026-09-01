from Estruturas.GerenciadorTxt import GerenciadorTxt
from Estruturas.Nodes import Node
from Estruturas.ArvoreB import ArvoreB
from Estruturas.Controlador import Controlador
from Estruturas.Registro import Registro

try:
    R = Registro(10,2,3,4,2,1)
except TypeError:
    print("Registro invalido, está faltando preencher todas as colunas")
