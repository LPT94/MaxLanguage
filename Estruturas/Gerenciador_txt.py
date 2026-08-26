import os

class Gerenciador_txt:

    def __init__(self, nome_arquivo: str):
        self.nome_arquivo = nome_arquivo
        self.lista_offsets = self.listar_offsets()
        self.ultimo_deletado = []
        
    def listar_offsets(self):
    #Responsável por abrir a tabela.txt e retornar uma lista com todos os offsets de cada linha
        lista_offsets = []
        try:
            with open("Tabelas/" + self.nome_arquivo, "r", encoding="utf-8") as arquivo:
                
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
        if offset not in self.lista_offsets:
            return registro
        
        try:
            with open("Tabelas/" + self.nome_arquivo, "r", encoding="utf-8") as arquivo:
                arquivo.seek(offset)
                registro = arquivo.readline()

        except FileNotFoundError:
            print("Arquivo não encontrado.")

        return registro

    def tamanho_linha(self, offset):
        return len(self.acessar_registro(offset).encode('utf-8'))

    def del_registro(self, offset):

        if offset not in self.lista_offsets:
            return False
        try:
            with open("Tabelas/" + self.nome_arquivo, "r+", encoding="utf-8") as arquivo:
                arquivo.seek(offset)
                self.ultimo_deletado.append(arquivo.readline())
                arquivo.seek(offset)
                arquivo.write("-1;")

            return True
        
        except FileNotFoundError:
            print("Aqruivo não encontrado.")
            return False

    def inserir_registro(self, registro):

        novo_offset = self.lista_offsets[-1] + self.tamanho_linha(self.lista_offsets[-1]) + 1
        try:
            with open("Tabelas/" + self.nome_arquivo, "r+", encoding="utf-8") as arquivo:
                arquivo.seek(novo_offset)
                arquivo.write(registro+'\n')

            self.lista_offsets.append(novo_offset)

        except FileNotFoundError:
            print("Aqruivo não encontrado.")

    def atualizar_arquivo(self):

        atualizar = False
        try:
            with open("Tabelas/" + self.nome_arquivo, "r+", encoding="utf-8") as arquivo:
                for i in range(len(self.lista_offsets)):
                    arquivo.seek(self.lista_offsets[i])
                    linha = arquivo.readline()
  
                    if linha[0:2] == "-1" and not atualizar:
                        atualizar = True
                        pos = self.lista_offsets[i]
                    
                    elif atualizar and linha[0:2] != "-1":
                        arquivo.seek(pos)
                        arquivo.write(linha)
                        tamanho = self.tamanho_linha(self.lista_offsets[i])
                        pos += tamanho

                if atualizar:
                    arquivo.seek(pos)
                    arquivo.truncate()

        except FileNotFoundError:
            print("Aqruivo não encontrado.")

    def reordenar_arquivo(self, texto):
    
        caminho_temp = f"Tabelas/"+self.nome_arquivo+".tmp"
        with open(caminho_temp, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)

        os.replace(caminho_temp, "Tabelas/"+self.nome_arquivo)