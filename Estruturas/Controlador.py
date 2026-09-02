from Estruturas.ArvoreB import ArvoreB
from Estruturas.GerenciadorTxt import GerenciadorTxt
from Estruturas.Nodes import Node
import os

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
            indice = int(self.__gerenciador_txt.acessar_registro(offset).split(";")[0])
            self.__arvore_indices.inserir_node(Node(indice, offset))
    
            self.__recursao(vetor, inicio, meio-1)
            self.__recursao(vetor, meio+1, fim)

    def contruir_arvore_indices(self):

        lista_offsets = self.__gerenciador_txt.listar_offsets_validos()
        self.__recursao(lista_offsets, 0, len(lista_offsets)-1)

    def mostrar_arvore(self, tipo="In-Order"):

        if tipo == "In-Order":
            self.__arvore_indices.print_in_order(self.__arvore_indices.get_root())
        elif tipo == "Pre-Order":
            self.__arvore_indices.print_pre_order(self.__arvore_indices.get_root())
        elif tipo == "Width":
            self.__arvore_indices.print_in_width()

    def buscar_indice(self, indice):

        node, pai = self.__arvore_indices.buscar_node(indice)
        return node

    def inserir_node_reg(self, registro):
        
        node = Node(registro.get_id(), -1)

        if not self.__arvore_indices.inserir_node(node):
            return False

        reg_editado = registro.get_reg_editado()
        offset = self._Controlador__gerenciador_txt.inserir_registro(reg_editado)

        if offset == -1:
            return False

        node.set_off(offset)
        return True

    def del_registro(self, indice):

        deletado = self._Controlador__arvore_indices.deletar_node(indice)
        if not deletado:
            return False

        return self._Controlador__gerenciador_txt.del_registro(deletado.get_offs())

    def atualizar_arq(self):
        return self._Controlador__gerenciador_txt.atualizar_arquivo()

    def __write_pre_order(self, node, arquivo_atual, arquivo_novo):

        
        if not node:
            return
        print("here")
        self.__write_pre_order(node.get_e(), arquivo_atual, arquivo_novo)

        arquivo_atual.seek(node.get_offs())
        registro = arquivo_atual.readline()
        arquivo_novo.write(registro)

        self.__write_pre_order(node.get_d(), arquivo_atual, arquivo_novo)

    def ordenar_arquivo(self):

        tabela = self.__gerenciador_txt.get_nome_arq()
        caminho_temp = f"Tabelas/" + tabela + ".tmp"
        with open(caminho_temp, "w", encoding="utf-8") as arquivo_novo:
            with open("Tabelas/" + tabela, "r", encoding="utf-8") as arquivo_atual:
                self.__write_pre_order(self.__arvore_indices.get_root(), arquivo_atual, arquivo_novo)
                
        os.replace(caminho_temp, "Tabelas/"+tabela)
    