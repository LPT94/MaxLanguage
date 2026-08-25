class Gerenciador_txt:

    def __init__(self, nome_arquivo: str):
        self.nome_arquivo = nome_arquivo

    def listar_offsets(self):
    #Responsável por abrir a tabela.txt e retornar uma lista com todos os offsets de cada linha
        pos_linhas = []
        try:
            with open("Tabelas/" + self.nome_arquivo, "r", encoding="utf-8") as arquivo:
                
                while True:
                    posicao = arquivo.tell()
                    linha = arquivo.readline()
                    
                    if not linha:
                        break

                    pos_linhas.append(posicao)

        except FileNotFoundError:
            print("Arquivo não encontrado.")

        return pos_linhas
    
    def acessar_offset(self, offset):
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
        return len(self.acessar_offset(offset).encode('utf-8'))
                