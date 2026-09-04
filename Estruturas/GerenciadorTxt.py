class GerenciadorTXT:

    def __init__(self, nome_arquivo: str):
        self._nome_arquivo = "Tabelas/" + nome_arquivo
        self._ultimo_offset = None
        self._tabela_vazia = True
        self._ordenar_offsets()

    def _ordenar_offsets(self):
        lista = self.listar_offsets()
        if not lista:
            self._ultimo_offset = 0
            self._tabela_vazia = True
        else:
            self._ultimo_offset = lista[-1]
            self._tabela_vazia = False

    def get_nome_arq(self):
        return self._nome_arquivo
        
    def listar_offsets(self):
    #Responsável por abrir a tabela.txt e retornar uma lista com todos os offsets de cada linha
        lista_offsets = []
        try:
            with open(self._nome_arquivo, "r", encoding="utf-8") as arquivo:
                while True:
                    posicao = arquivo.tell()
                    linha = arquivo.readline()
                    
                    if not linha:
                        break

                    lista_offsets.append(posicao)

        except FileNotFoundError:
            print("Arquivo não encontrado.")

        return lista_offsets

    def listar_offsets_validos(self):
        lista_offsets = []
        try:
            with open(self._nome_arquivo, "r", encoding="utf-8") as arquivo:
                while True:
                    posicao = arquivo.tell()
                    linha = arquivo.readline()
                    
                    if not linha:
                        break

                    if linha.split(";")[0] != "-1":
                        lista_offsets.append(posicao)

        except FileNotFoundError:
            print("Arquivo não encontrado.")

        return lista_offsets

    def acessar(self, offset):
    #Responsável por retornar uma string com uma linha completa do offset
        registro = ""
        try:
            with open(self._nome_arquivo, "r", encoding="utf-8") as arquivo:
                arquivo.seek(offset)
                registro = arquivo.readline()

        except FileNotFoundError:
            print("Arquivo não encontrado.")

        return registro

    def tamanho(self, offset):
        return len(self.acessar(offset).encode('utf-8'))

    def deletar(self, offset):

        try:
            with open(self._nome_arquivo, "r+", encoding="utf-8") as arquivo:
                arquivo.seek(offset)
                arquivo.seek(offset)
                arquivo.write("-1;")

            return True
        
        except FileNotFoundError:
            print("Arquivo não encontrado.")
            return False

    def inserir(self, registro):

        if self._tabela_vazia:
            novo_offset = 0
            self._tabela_vazia = False
        else:
            novo_offset =  self._ultimo_offset + self.tamanho(self._ultimo_offset) + 1

        try:
            with open(self._nome_arquivo, "r+", encoding="utf-8") as arquivo:
                arquivo.seek(novo_offset)
                arquivo.write(registro+'\n')
                print(novo_offset)
                self._ultimo_offset = novo_offset

            return novo_offset

        except FileNotFoundError:
            print("Arquivo não encontrado.")
            return -1

    def atualizar(self):

        atualizar = False
        try:
            with open(self._nome_arquivo, "r+", encoding="utf-8") as arquivo:
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
                        tamanho = self.tamanho(lista[i])
                        pos += tamanho + 1

                if atualizar:
                    arquivo.seek(pos)
                    arquivo.truncate()
                    self._ordenar_offsets()

                return True
            
        except FileNotFoundError:
            print("Arquivo não encontrado.")
            return False

    