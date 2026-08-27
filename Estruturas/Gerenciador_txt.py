import os

class Gerenciador_txt:

    def __init__(self, nome_arquivo: str):
        self.__nome_arquivo = nome_arquivo

        lista = self.listar_offsets()
        if not lista:
            self.__ultimo_offset = 0
            self.__tabela_vazia = True
        else:
            self.__ultimo_offset = lista[-1]
            self.__tabela_vazia = False
            
        self.__ultimos_offsets_deletados = []
        
    def listar_offsets(self):
    #Responsável por abrir a tabela.txt e retornar uma lista com todos os offsets de cada linha
        lista_offsets = []
        try:
            with open("Tabelas/" + self.__nome_arquivo, "r", encoding="utf-8") as arquivo:
                while True:
                    posicao = arquivo.tell()
                    linha = arquivo.readline()
                    
                    if not linha:
                        break

                    lista_offsets.append(posicao)

        except FileNotFoundError:
            print("Arquivo não encontrado.")

        return lista_offsets

    def acessar_registro(self, offset):
    #Responsável por retornar uma string com uma linha completa do offset
        registro = ""
        try:
            with open("Tabelas/" + self.__nome_arquivo, "r", encoding="utf-8") as arquivo:
                arquivo.seek(offset)
                registro = arquivo.readline()

        except FileNotFoundError:
            print("Arquivo não encontrado.")

        return registro

    def tamanho_registro(self, offset):
        return len(self.acessar_registro(offset).encode('utf-8'))

    def del_registro(self, offset):

        try:
            with open("Tabelas/" + self.__nome_arquivo, "r+", encoding="utf-8") as arquivo:
                arquivo.seek(offset)
                self.__ultimos_offsets_deletados.append(arquivo.readline())
                arquivo.seek(offset)
                arquivo.write("-1;")

        except FileNotFoundError:
            print("Aqruivo não encontrado.")

    def inserir_registro(self, registro):

        if self.__tabela_vazia:
            novo_offset = 0
            self.__tabela_vazia = False
        else:
            novo_offset =  self.__ultimo_offset + self.tamanho_registro(self.__ultimo_offset) + 1

        try:
            with open("Tabelas/" + self.__nome_arquivo, "r+", encoding="utf-8") as arquivo:
                arquivo.seek(novo_offset)
                arquivo.write(registro+'\n')
                self.__ultimo_offset = novo_offset

        except FileNotFoundError:
            print("Aqruivo não encontrado.")

    def atualizar_arquivo(self):

        atualizar = False
        try:
            with open("Tabelas/" + self.__nome_arquivo, "r+", encoding="utf-8") as arquivo:
                lista = self.listar_offsets()
                for i in range(len(lista)):
                    arquivo.seek(lista[i])
                    linha = arquivo.readline()

                    
                    if linha[0:2] == "-1" and not atualizar:
                        atualizar = True
                        pos = lista[i]
                    
                    elif atualizar and linha[0:2] != "-1":
                        arquivo.seek(pos)
                        arquivo.write(linha)
                        tamanho = self.tamanho_registro(lista[i])
                        pos += tamanho + 1

                if atualizar:
                    arquivo.seek(pos)
                    arquivo.truncate()

        except FileNotFoundError:
            print("Aqruivo não encontrado.")

    def reordenar_arquivo(self, texto):
    
        caminho_temp = f"Tabelas/" + self.__nome_arquivo + ".tmp"
        with open(caminho_temp, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)

        os.replace(caminho_temp, "Tabelas/"+self.__nome_arquivo)