from Controllers.Controlador import Controlador
from Registers.RegistroIdiomas import RegistroIdiomas

class ControladorIdiomas(Controlador):

    def __init__(self, nome_arquivo):
        super().__init__(nome_arquivo)


    def validar_dados(self, registro):
        validacao, mensagem = self._eh_int([registro.get_id()], ['id'])
        if not validacao:
            return validacao, mensagem

        validacao, mensagem = self._caracter_valido([registro.get_descricao()], ['descricao'])
        if not validacao:
            return validacao, mensagem

        return True, "Dados validados."


    def validar_constraints_insert(self, registro):
        if not self.unique(registro.get_descricao(), 1):
            return False, "Descrição já existente."

        return True, "Constraints validadas."


    def validar_cascade(self, lista_referencia):
        if lista_referencia[0]:
            return False, "Não é permitido deletar este idioma pois existem lições registradas neste idioma."

        if lista_referencia[1]:
            return False, "Não é permitido deletar este idioma pois existem usuários registrados neste idioma."

        return True, "Constraints validadas"


    def get_registro(self, indice):
    
        node = self.buscar_node(int(indice))
        if not node:
            return None, node
        
        dados_brutos = self._gerenciador_txt.acessar(node.get_offs())
        dados = dados_brutos.strip().split(";")
        registro = RegistroIdiomas(dados[0], dados[1])

        return registro


    def listar_registros(self):

        lista_registros = []
        lista_dados = self.listar_dados()

        for i in range(len(lista_dados)):
            lista_registros.append(RegistroIdiomas(lista_dados[i][0], lista_dados[i][1]))

        return lista_registros
    
