from Controllers.Controlador import Controlador
from Registers.RegistroIdiomas import RegistroIdiomas

class ControladorIdiomas(Controlador):

    def __init__(self, nome_arquivo):
        super().__init__(nome_arquivo)

    def validar_dados(self, registro):

        if not self._eh_int([registro.get_id()], ['id']):
            return False

        if not self._caracter_valido([registro.get_descricao()], ['descricao']):
            return False

        return True


    def validar_constraints(self, registro):
        
        if not self.unique(registro.get_descricao(), 1):
            print("Erro! Atributo descrição deve ser único")
            return False

        return True

    def get_registro(self, indice):
    
        node = self.buscar_node(indice)
        if not node:
            return None, node
        
        dados_brutos = self._gerenciador_txt.acessar(node.get_offs())
        dados = dados_brutos.strip().split(";")
        registro = RegistroIdiomas(dados[0], dados[1])

        return registro, node

    def listar_registros(self):

        lista_registros = []
        lista_dados = self.listar_dados()

        for i in range(len(lista_dados)):
            lista_registros.append(RegistroIdiomas(lista_dados[i][0], lista_dados[i][1]))

        return lista_registros
    
