from Estruturas.Controlador import Controlador
from Estruturas.RegistroExercicios import RegistroExercicios

class ControladorExercicios(Controlador):

    def __init__(self, nome_arquivo, controlador_licoes):
        super().__init__(nome_arquivo)
        self._controlador_licoes = controlador_licoes

    def validar_constraints(self, registro):

        no_estrangeiro = self._controlador_licoes.buscar_node(registro.get_licao())
        if not no_estrangeiro:
            print("Erro! Foreign Key não encontrada na tabela lições.")
            return False

        nivel = registro.get_nivel()
        if nivel < 1:
            print("Erro! Atributo nivel tem que ser maior que zero.")
            return False

        reg_licoes = self._controlador_licoes.get_registro(no_estrangeiro.get_i())
        print(reg_licoes.get_total_niveis())
        if nivel > reg_licoes.get_total_niveis():
            print("Erro! Atributo nivel tem que ser menor ou igual ao total de niveis do registro lição")
            return False

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
        dados = dados_brutos.strip().split(";")
        registro = RegistroExercicios(dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], 
                                      dados[6], dados[7], dados[8], dados[9])

        return registro

