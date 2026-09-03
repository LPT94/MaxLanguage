from Estruturas.Controlador import Controlador
from Estruturas.RegistroExercicios import RegistroExercicios
from Estruturas.Nodes import Node

class ControladorExercicios(Controlador):

    def __init__(self, nome_arquivo, controlador_licoes):
        super().__init__(nome_arquivo)
        self._controlador_licoes = controlador_licoes

    def validar(self, registro):
        if registro.get_id() < 1:
            print("Erro! Primary key inválida.")
            return False
        
        no_estrangeiro = self._controlador_licoes.buscar_node(registro.get_licao())
        if not no_estrangeiro:
            print("Erro! Foreign Key não encontrada na tabela lições.")
            return False

        #TODO: verificar se nivel <= total_niveis do registro lição. No entanto, antes é necessário criar a classe ControladorLicoes

        op_correta = registro.get_op_correta()
        if op_correta > 7 or op_correta < 4:
            print("Erro! Atributo opção correta inválido.")
            return False 

        return True

    def get_registro(self, indice):

        node = self.buscar_node(indice)
        if not node:
            return None
        
        dados_brutos = self._gerenciador_txt.acessar(node.get_offs())
        dados = dados_brutos.split(";")
        registro = RegistroExercicios(dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], 
                                      dados[6], dados[7], dados[8], dados[9])

        return registro

