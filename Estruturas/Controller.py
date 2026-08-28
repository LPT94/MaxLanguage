from Estruturas.ArvoreB import ArvoreB
from Estruturas.GerenciadorTxt import GerenciadorTxt
from Estruturas.Nodes import Node

class Controller:

    def __init__(self, nome_arquivo):
        self.__gerenciador_txt = GerenciadorTxt(nome_arquivo)
        self.__arvore_indices = ArvoreB(None)

    def contruir_arvore_indices(self):

        lista_offsets = self.__gerenciador_txt.listar_offsets()

        for i in range(len(lista_offsets)):
            offset = lista_offsets[i]
            indice = int(self.__gerenciador_txt.acessar_registro(offset).split(";")[0])
            self.__arvore_indices.inserir_node(Node(indice, offset))

    def show_tree(self, tipo):

        if tipo == "In-Order":
            self.__arvore_indices.print_in_order(self.__arvore_indices.get_root())
        elif tipo == "Pre-Order":
            self.__arvore_indices.print_pre_order(self.__arvore_indices.get_root())

    def get_root(self):
        return self.__arvore_indices.get_root()