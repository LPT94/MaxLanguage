class GerenciadorTXT:

    def __init__(self, nome_arquivo: str):
        self._nome_arquivo = "Tabelas/" + nome_arquivo
        self._tamanho_inicial = 0
        self._tabela_vazia = True
        self._ultimo_offset = 0

        self._start()

    def _start(self):
        lista_registros = self.listar_offsets()

        self._tamanho_inicial = len(lista_registros)
        self._tabela_vazia = not bool(self._tamanho_inicial)
        self._ultimo_offset = self._calular_ultimo_offset(lista_registros)

    def _calular_ultimo_offset(self, lista_registros):
        if not lista_registros:
            return 0
        else:
            return lista_registros[-1]

    def get_tamanho_inicial(self):
        return self._tamanho_inicial

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

    def listar_offsets_ids_validos(self):
        lista_offsets_ids = []
        try:
            with open(self._nome_arquivo, "r", encoding="utf-8") as arquivo:
                while True:
                    posicao = arquivo.tell()
                    linha = arquivo.readline()
                    
                    if not linha:
                        break

                    atributos = linha.split(";")
                    if atributos[0] != "-1":

                        lista_offsets_ids.append([posicao, atributos[0]])

        except FileNotFoundError:
            print("Arquivo não encontrado.")

        return lista_offsets_ids


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
                self._ultimo_offset = novo_offset

            return novo_offset

        except FileNotFoundError:
            print("Arquivo não encontrado.")
            return -1
    