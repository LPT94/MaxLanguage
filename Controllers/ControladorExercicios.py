from Controllers.Controlador import Controlador
from Registers.RegistroExercicios import RegistroExercicios

class ControladorExercicios(Controlador):

    def __init__(self, nome_arquivo, controlador_licoes):
        super().__init__(nome_arquivo)
        self._controlador_licoes = controlador_licoes

    
    def validar_dados(self, registro):

        opcao_correta = registro.get_op_correta()
        pontuacao = registro.get_pontuacao()

        validacao, mensagem = self._eh_int([registro.get_id(), registro.get_licao(), registro.get_nivel(), 
                            opcao_correta, pontuacao],
                            ['id', 'codigo licao', 'nivel', 'opção correta', 'pontuação'])

        if not validacao:
            return validacao, mensagem

        validacao, mensagem = self._caracter_valido([registro.get_descricao(), registro.get_op_a(), registro.get_op_b(), 
                                       registro.get_op_c(), registro.get_op_d()],
                                       ['descricao', 'opção A', 'opção B', 'opção C', 'opção D'])

        if not validacao:
            return validacao, mensagem
        
        if int(opcao_correta) > 7 or int(opcao_correta) < 4:
            return False, "O valor da opção correta deve ser entre 4 e 7."

        if int(pontuacao) < 1:
            return False, "Pontuação deve ser maior que 0."

        return True, "Dados validados."

    def validar_constraints(self, registro):

        no_estrangeiro = self._controlador_licoes.buscar_node(int(registro.get_licao()))
        if not no_estrangeiro:
            return False, "Lição não encontrada."

        nivel = int(registro.get_nivel())

        if nivel < 1:
            return False, "Nível deve ser maior que 0."
    
        reg_licoes, node = self._controlador_licoes.get_registro(no_estrangeiro.get_i())
        if nivel > int(reg_licoes.get_total_niveis()):
            return False, "Nível deve ser maior ou igual ao total de nível da Lição."

        return True, "Constraints validadas."

    def get_registro(self, indice):

        node = self.buscar_node(int(indice))
        if not node:
            return None, node
        
        dados_brutos = self._gerenciador_txt.acessar(node.get_offs())
        dados = dados_brutos.strip().split(";")
        registro = RegistroExercicios(dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], 
                                      dados[6], dados[7], dados[8], dados[9])

        return registro, node

