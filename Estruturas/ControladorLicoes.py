from Estruturas.Controlador import Controlador
from Estruturas.RegistroLicoes import RegistroLicoes

class ControladorLicoes(Controlador):

    def __init__(self, nome_arquivo, controlador_idioma):
        super().__init__(nome_arquivo)
        self._controlador_idioma = controlador_idioma

    def validar_constraints(self, registro):
        
        no_estrangeiro = self._controlador_idioma.buscar_node(registro.get_cod_idioma())
        if not no_estrangeiro:
            print("Erro! Foreign Key não encontrada na tabela Idioma.")
            return False

        return True

    def get_registro(self, indice):
    
        node = self.buscar_node(indice)
        if not node:
            return None, node
        
        dados_brutos = self._gerenciador_txt.acessar(node.get_offs())
        dados = dados_brutos.strip().split(";")
        registro = RegistroLicoes(dados[0], dados[1], dados[2])

        return registro, node