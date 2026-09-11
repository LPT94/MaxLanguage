from Controllers.Controlador import Controlador
from Registers.RegistroLicoes import RegistroLicoes

class ControladorLicoes(Controlador):

    def __init__(self, nome_arquivo, controlador_idioma):
        super().__init__(nome_arquivo)
        self._controlador_idioma = controlador_idioma

    def validar_dados(self, registro):

        total_niveis = registro.get_total_niveis()

        if not self._eh_int([registro.get_id(), registro.get_cod_idioma(), total_niveis],
                            ['id', 'codigo idioma', 'total níveis']):
            return False

        if int(total_niveis) < 1:
            print("Erro! Total de níveis inválido.")
            return False

        return True

    
    def validar_constraints(self, registro):
        
        no_estrangeiro = self._controlador_idioma.buscar_node(int(registro.get_cod_idioma()))
        if not no_estrangeiro:
            print("Erro! Foreign Key não encontrada na tabela Idioma.")
            return False

        return True

    def get_registro(self, indice):
    
        node = self.buscar_node(int(indice))
        if not node:
            return None, node
        
        dados_brutos = self._gerenciador_txt.acessar(node.get_offs())
        dados = dados_brutos.strip().split(";")
        registro = RegistroLicoes(dados[0], dados[1], dados[2])

        return registro, node