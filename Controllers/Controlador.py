from Estruturas.ArvoreB import ArvoreB
from Estruturas.GerenciadorTxt import GerenciadorTXT
from Estruturas.Nodes import Node
import os

class Controlador:

    def __init__(self, nome_arquivo):
        self._gerenciador_txt = GerenciadorTXT(nome_arquivo)
        self._arvore_indices = ArvoreB(None)

        lista_offsets_validos = self._gerenciador_txt.listar_offsets_ids_validos()
        self.__construir_arvore_indices(lista_offsets_validos, 0, len(lista_offsets_validos)-1)

        self._inseridos = 0
        self._total = self._gerenciador_txt.get_tamanho_inicial()
        self._fora_de_ordem = self.__ids_fora_de_ordem(lista_offsets_validos)
        self._deletados = self._total - len(lista_offsets_validos)
        self._proximo_id = self._calcular_proximo_id()


    def get_total(self):
        return self._total


    def get_inseridos(self):
        return self._inseridos


    def get_fora_ordem(self):
        return self._fora_de_ordem


    def get_deletados(self):
        return self._deletados


    def get_proximo_id(self):
        return self._proximo_id


    def __ids_fora_de_ordem(self, lista_offsets):
        if not lista_offsets:
            return 0
        
        last = -1
        fora_ordem = 0
        for offset, indice in lista_offsets:
            if int(indice) < last:
                fora_ordem += 1
            last = int(indice)

        return fora_ordem


    def _calcular_proximo_id(self):
        node = self._arvore_indices.get_root()
        if not node:
            return 1

        while node.get_d():
            node = node.get_d()

        return node.get_i()+1


    def __construir_arvore_indices(self, vetor, inicio, fim):
        if inicio > fim:
            return

        meio = (fim - inicio) // 2 + inicio
        offset = int(vetor[meio][0])
        indice = int(vetor[meio][1])
        self._arvore_indices.inserir(Node(indice, offset))

        self.__construir_arvore_indices(vetor, inicio, meio-1)
        self.__construir_arvore_indices(vetor, meio+1, fim)


    def mostrar_arvore(self, tipo="In-Order"):

        if tipo == "In-Order":
            self._arvore_indices.print_in_order(self._arvore_indices.get_root())
        elif tipo == "Pre-Order":
            self._arvore_indices.print_pre_order(self._arvore_indices.get_root())
        elif tipo == "Width":
            self._arvore_indices.print_in_width()

        print()


    def buscar_node(self, indice):
        node, pai = self._arvore_indices.buscar(indice)
        return node


    def validar_pk(self, registro):
        if int(registro.get_id()) < 1:
            return False, "Id inválida."
        
        return True, "Id válida."


    def _caracter_valido(self, lista_atributo, lista_nome):
        for i in range(len(lista_atributo)):
            if ";" in lista_atributo[i] or "\n" in lista_atributo[i] or "\r" in lista_atributo[i]:
                return False, f"{lista_nome[i]} contém caracteres inválidos."
            
        return True, "Caracteres válidos."


    def _eh_int(self, lista_int, lista_nome):
        for i in range(len(lista_int)):
            try:
                int(lista_int[i])
            except ValueError:
                return False, f"{lista_nome[i]} deve ser um número inteiro positivo."

        return True, "Valor válido."


    def inserir_registro(self, registro):
        sucesso, mensagem = self.validar_dados(registro)
        if not sucesso:
            return sucesso, mensagem

        sucesso, mensagem = self.validar_pk(registro)
        if not sucesso:
            return sucesso, mensagem

        sucesso, mensagem = self.validar_constraints(registro)
        if not sucesso:
            return sucesso, mensagem

        node = Node(int(registro.get_id()), -1)
        if not self._arvore_indices.inserir(node):
            return False, "Indice já existente."

        reg_formatado = registro.formatar()

        offset = self._gerenciador_txt.inserir(reg_formatado)

        if offset == -1:
            self._arvore_indices.deletar(int(registro.get_id()))
            return False, "Erro na manipulação do arquivo ou arquivo não encontrado."

        node.set_off(offset)
        self._proximo_id += 1
        self._total += 1
        self._inseridos += 1

        if self._deve_atualizar_arvore():
            self._atualizar_arvore()

        return True, "Registro inserido com sucesso."


    def editar_registro(self, registro, controlador=None):
        sucesso, mensagem = self.validar_dados(registro)
        if not sucesso:
            return sucesso, mensagem

        sucesso, mensagem = self.validar_pk(registro)
        if not sucesso:
            return sucesso, mensagem
        
        sucesso, mensagem = self.validar_constraints_insert(registro)
        if not sucesso:
            return sucesso, mensagem

        if controlador:
            sucesso, mensagem = self._validar_constraints_edit(controlador)
            if not sucesso:
                return sucesso, mensagem

        node = self.buscar_node(int(registro.get_id()))
        if node is None:
            return False, "Registro não encontrado."
        
        reg_formatado = registro.formatar()

        offset = self._gerenciador_txt.inserir(reg_formatado)

        if offset == -1:
            return False, "Erro na manipulação do arquivo ou arquivo não encontrado."

        sucesso = self._gerenciador_txt.deletar(node.get_offs())
        if not sucesso:
            return False, "Erro na manipulação do arquivo ou arquivo não encontrado."
        
        node.set_off(offset)
        if node.get_i() != self._proximo_id - 1:
            self._fora_de_ordem += 1

        self._deletados += 1
        self._total += 1

        if self._deve_ordenar_arquivo():
            self.ordenar_arquivo()
            self._atualizar_arvore()

        return True, "Registro editado com sucesso."


    def del_registro(self, indice, lista_infos):
        sucesso, mensagem = self.validar_cascade(lista_infos)
        if not sucesso:
            return sucesso, mensagem
        
        node_del = self._arvore_indices.deletar(int(indice))
        if not node_del:
            return False, "Índice não encontrado."

        sucesso = self._gerenciador_txt.deletar(node_del.get_offs())
        if not sucesso:
            self._arvore_indices.inserir(node_del)
            return False, "Erro na manipulação do arquivo ou arquivo não encontrado."

        self._deletados += 1

        if self._deve_ordenar_arquivo():
            self.ordenar_arquivo()
            self._atualizar_arvore()

        return True, "Registro deletado com sucesso."


    def unique(self, atributo, indice_atributo):
        lista_registros = self._gerenciador_txt.listar_offsets_ids_validos()
        arquivo = open(self._gerenciador_txt.get_nome_arq(), "r", encoding="utf-8")

        for offset, id in lista_registros:
            arquivo.seek(offset)
            dados = arquivo.readline().strip().split(";")
            if dados[indice_atributo] == atributo:
                arquivo.close()
                return False

        arquivo.close()
        return True


    def listar_atributos(self, atributos):      #TODO: verificar se este método realmente é necessário
        lista_offsets = self._gerenciador_txt.listar_offsets_ids_validos()
        matriz_dados = [[0] * len(lista_offsets) for _ in range(len(atributos))]
        j = 0

        arquivo = open(self._gerenciador_txt.get_nome_arq(), "r", encoding="utf-8")
        for offset, id in lista_offsets:
            arquivo.seek(offset)
            dados = arquivo.readline().strip().split(";")
            for i in range(len(atributos)):
                matriz_dados[j][i] = dados[atributos[i]]

            j+= 1
        arquivo.close()
        return matriz_dados


    def __existe_referencia(self, node, arquivo, indice_atributo, valor):
        if node is None:
            return False

        arquivo.seek(node.get_offs())
        dados = arquivo.readline().strip().split(";")
        if dados[indice_atributo] == str(valor):
            return True

        else:
            res = self.__existe_referencia(node.get_e(), arquivo, indice_atributo, valor)
            if not res:
                return self.__existe_referencia(node.get_d(), arquivo, indice_atributo, valor)

            return res

        
    def verifica_referencia(self, indice_atributo, valor):
        arquivo = open(self._gerenciador_txt.get_nome_arq(), "r", encoding="utf-8")
        res =  self.__existe_referencia(self._arvore_indices.get_root(), arquivo, indice_atributo, valor)
        arquivo.close()
        return res


    def __listar_in_order(self, arquivo, node, lista):
        if node is None:
            return

        self.__listar_in_order(arquivo, node.get_e(), lista)

        arquivo.seek(node.get_offs())
        dados = arquivo.readline().strip().split(";")
        lista.append(dados)

        self.__listar_in_order(arquivo, node.get_d(), lista)

    def listar_dados(self):
        lista = []
        arquivo = open(self._gerenciador_txt.get_nome_arq(), "r", encoding="utf-8")
        self.__listar_in_order(arquivo, self._arvore_indices.get_root(), lista)
        arquivo.close()
        return lista


    def registros_com_criterio(self, criterios):
        lista_registros = self._gerenciador_txt.listar_offsets_ids_validos()
        resultados = []
        arquivo = open(self._gerenciador_txt.get_nome_arq(), "r", encoding="utf-8")
        for offset, id in lista_registros:
            flag = True
            arquivo.seek(offset)
            dados = arquivo.readline().strip().split(";")
            for chave in criterios.keys():
                if dados[chave] != criterios[chave]:
                    flag = False
                    break

                flag = True  

            if flag:
                resultados.append(dados)

        arquivo.close()
        return resultados


    def _deve_atualizar_arvore(self):
        if self._total > 20 and self._inseridos > self._total * 0.2:
            return True

        return False

    
    def _deve_ordenar_arquivo(self):
        if self._total > 20 and (self._fora_de_ordem > self._total * 0.2 or self._deletados > self._total * 0.2):
            return True

        return False


    def _atualizar_arvore(self):
        self._inseridos = 0
        lista_offsets_validos = self._gerenciador_txt.listar_offsets_ids_validos()
        self._arvore_indices.limpar_arvore()
        self.__construir_arvore_indices(lista_offsets_validos, 0, len(lista_offsets_validos)-1)


    def __escrever_in_order(self, node, arquivo_atual, arquivo_novo):
        if not node:
            return
        
        self.__escrever_in_order(node.get_e(), arquivo_atual, arquivo_novo)

        arquivo_atual.seek(node.get_offs())
        registro = arquivo_atual.readline()
        arquivo_novo.write(registro)

        self.__escrever_in_order(node.get_d(), arquivo_atual, arquivo_novo)


    def ordenar_arquivo(self):
        caminho_atual = self._gerenciador_txt.get_nome_arq()
        caminho_tmp = caminho_atual + ".tmp"
        arquivo_atual = open(caminho_atual, "r", encoding="utf-8")
        arquivo_sub = open(caminho_tmp, "w", encoding="utf-8")
        self.__escrever_in_order(self._arvore_indices.get_root(), arquivo_atual, arquivo_sub)
        arquivo_atual.close()
        arquivo_sub.close()

        os.replace(caminho_tmp, caminho_atual)
        self._gerenciador_txt._start()
        self._total -= self._deletados
        self._deletados = 0
        self._fora_de_ordem = 0
    