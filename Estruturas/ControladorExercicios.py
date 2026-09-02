from Estruturas.Controlador import Controlador
from Estruturas.RegistroExercicios import RegistroExercicios
from Estruturas.Nodes import Node

class ControladorExercicios(Controlador):

    def __init__(self, nome_arquivo):
        super().__init__(nome_arquivo)

    def __validacoes(self, registro, controlador_licoes):
        no_estrangeiro = controlador_licoes.buscar_indice(registro.get_licao())
        if not no_estrangeiro:
            print("Erro! Foreign Key não encontrada na tabela lições.")
            return False

        op_correta = registro.get_op_correta()
        if op_correta > 7 or op_correta < 4:
            print("Erro! Atributo opção correta inválido.")
            return False 

        return True
    
    def inserir(self, registro, controlador_licoes):

        if not self.__validacoes(registro, controlador_licoes):
            return False
        
        return self.inserir_node_reg(registro)
