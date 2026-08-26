import os

class Gerenciador_txt:

    def __init__(self, nome_arquivo: str):
        self.nome_arquivo = nome_arquivo
        self.ultimo_deletado = []
        self.ultimo_offset = self.listar_offsets()[-1]

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
        try:
            with open("Tabelas/" + self.nome_arquivo, "r+", encoding="utf-8") as arquivo:
                arquivo.seek(offset)
                self.ultimo_deletado.append(arquivo.readline())
                arquivo.seek(offset)
                arquivo.write("-1;")

        except FileNotFoundError:
            print("Aqruivo não encontrado.")

    def inserir_registro(self, registro):
        try:
            with open("Tabelas/" + self.nome_arquivo, "r+", encoding="utf-8") as arquivo:
                arquivo.seek(self.ultimo_offset)
                arquivo.write(registro+'\n')
                self.ultimo_offset += len(registro.encode('utf-8'))+1
                
        except FileNotFoundError:
            print("Aqruivo não encontrado.")

    def atualizar_arquivo(self):

        lista_offsets = self.listar_offsets()
        atualizar = False

        try:
            with open("Tabelas/" + self.nome_arquivo, "r+", encoding="utf-8") as arquivo:
                for i in range(len(lista_offsets)):
                    arquivo.seek(lista_offsets[i])
                    linha = arquivo.readline()
  
                    if linha[0:2] == "-1" and not atualizar:
                        atualizar = True
                        pos = lista_offsets[i]
                    
                    elif atualizar and linha[0:2] != "-1":
                        arquivo.seek(pos)
                        arquivo.write(linha)
                        tamanho = self.tamanho_linha(lista_offsets[i])
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