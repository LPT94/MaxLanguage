from Estruturas.ArvoreB import ArvoreB
from Estruturas.GerenciadorTxt import GerenciadorTxt
from Estruturas.Nodes import Node

class Controlador:

    def __init__(self, nome_arquivo):
        self.__gerenciador_txt = GerenciadorTxt(nome_arquivo)
        self.__arvore_indices = ArvoreB(None)

    def get_root(self):
        return self.__arvore_indices.get_root()

    def __recursao(self, vetor, inicio, fim):
            if inicio > fim:
                return
    
            meio = (fim - inicio) // 2 + inicio

            offset = vetor[meio]
            indice = self.__gerenciador_txt.acessar_registro(offset).split(";")[0]
            self.__arvore_indices.inserir_node(Node(indice, offset))
    
            self.__recursao(vetor, inicio, meio-1)
            self.__recursao(vetor, meio+1, fim)

    def contruir_arvore_indices(self):

        lista_offsets = self.__gerenciador_txt.listar_offsets()
        self.__recursao(lista_offsets, 0, len(lista_offsets)-1)

    def mostrar_arvore(self, tipo):

        if tipo == "In-Order":
            self.__arvore_indices.print_in_order(self.__arvore_indices.get_root())
        elif tipo == "Pre-Order":
            self.__arvore_indices.print_pre_order(self.__arvore_indices.get_root())
        elif tipo == "Width":
            self.__arvore_indices.print_in_width()



    