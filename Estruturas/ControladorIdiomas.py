from Estruturas.Controlador import Controlador
from Estruturas.RegistroIdiomas import RegistroIdiomas

class ControladorIdiomas(Controlador):

    def __init__(self, nome_arquivo):
        super().__init__(nome_arquivo)

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
    
