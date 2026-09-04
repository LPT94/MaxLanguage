from Estruturas.ArvoreB import ArvoreB
from Estruturas.GerenciadorTXT import GerenciadorTXT
from Estruturas.Nodes import Node
import os

class Controlador:

    def __init__(self, nome_arquivo):
        self._gerenciador_txt = GerenciadorTXT(nome_arquivo)
        self._arvore_indices = ArvoreB(None)

    def __recursao(self, vetor, inicio, fim):
            if inicio > fim:
                return
    
            meio = (fim - inicio) // 2 + inicio

            offset = vetor[meio]
            indice = int(self._gerenciador_txt.acessar(offset).split(";")[0])
            self._arvore_indices.inserir(Node(indice, offset))
    
            self.__recursao(vetor, inicio, meio-1)
            self.__recursao(vetor, meio+1, fim)

    def contruir_arvore_indices(self):

        lista_offsets = self._gerenciador_txt.listar_offsets_validos()
        self.__recursao(lista_offsets, 0, len(lista_offsets)-1)

    def mostrar_arvore(self, tipo="In-Order"):

        if tipo == "In-Order":
            self._arvore_indices.print_in_order(self._arvore_indices.get_root())
        elif tipo == "Pre-Order":
            self._arvore_indices.print_pre_order(self._arvore_indices.get_root())
        elif tipo == "Width":
            self._arvore_indices.print_in_width()

    def buscar_node(self, indice):        #TODO: verificar depois se esta função é útil

        node, pai = self._arvore_indices.buscar(indice)
        return node

    def inserir_registro(self, registro):

        if not self.validar(registro):
            return False

        node = Node(registro.get_id(), -1)

        if not self._arvore_indices.inserir(node):
            return False

        reg_formatado = registro.formatar()

        offset = self._gerenciador_txt.inserir(reg_formatado)

        if offset == -1:
            return False

        node.set_off(offset)
        return True

    def del_registro(self, indice):

        deletado = self._arvore_indices.deletar(indice)
        if not deletado:
            return False

        return self._gerenciador_txt.deletar(deletado.get_offs())

    def atualizar_arquivo(self):
        #Após atualizar o arquivo se for continuar atualizando a classe 
        # é necessária atualizar a arvore de indices
        return self._gerenciador_txt.atualizar()

    def __escrever_pre_order(self, node, arquivo_atual, arquivo_novo):

        if not node:
            return
        
        self.__escrever_pre_order(node.get_e(), arquivo_atual, arquivo_novo)

        arquivo_atual.seek(node.get_offs())
        registro = arquivo_atual.readline()
        arquivo_novo.write(registro)

        self.__escrever_pre_order(node.get_d(), arquivo_atual, arquivo_novo)

    def ordenar_arquivo(self):
        #Função elaborada para ser chamada quando encerrar o programa.
        #Após ordernar o arquivo, se for continuar utilizando a classe, para ganho de desempenho
        #é necessário atualizar a arvore de indices

        caminho_atual = self._gerenciador_txt.get_nome_arq()
        caminho_tmp = caminho_atual + ".tmp"
        arquivo_atual = open(caminho_atual, "r", encoding="utf-8")
        arquivo_sub = open(caminho_tmp, "w", encoding="utf-8")
        self.__escrever_pre_order(self._arvore_indices.get_root(), arquivo_atual, arquivo_sub)
        arquivo_atual.close()
        arquivo_sub.close()

        os.replace(caminho_tmp, caminho_atual)
        self._gerenciador_txt._ordenar_offsets()
    