from Controllers.Controlador import Controlador
from Registers.RegistroLicoes import RegistroLicoes

class ControladorLicoes(Controlador):

    def __init__(self, nome_arquivo, controlador_idioma):
        super().__init__(nome_arquivo)
        self._controlador_idioma = controlador_idioma


    def validar_dados(self, registro):
        total_niveis = registro.get_total_niveis()

        if not self._eh_int([registro.get_id(), registro.get_cod_idioma(), total_niveis],
                            ['Id', 'Codigo Idioma', 'Total Níveis']):
            return False

        if int(total_niveis) < 1:
            return False, "Total Níveis deve ser maior que 0"

        return True, "Dados válidos."


    def validar_constraints_insert(self, registro):
        no_estrangeiro = self._controlador_idioma.buscar_node(int(registro.get_cod_idioma()))
        if not no_estrangeiro:
            print("Erro! Foreign Key não encontrada na tabela Idioma.")
            return False, "Idioma selecionado não encontrado."

        return True, "Constraints validadas."


    def validar_constraints_edit(self, registro, controlador):
        lista_registros = controlador.registros_com_criterio({2:registro.get_id()})
        novo_nivel = registro.get_total_niveis()
        for reg in lista_registros:
            if reg.get_nivel() > novo_nivel:
                return False, f"O exercício de código {reg.get_id()} pertence à um nível maior que o nível selecionado."

        return True, "Constraints validadas"


    def validar_cascade(self, lista_referencia):
            if lista_referencia[0]:
                return False, "Não é permitido deletar esta lição pois existem exercícios registrados nela."
    
            return True, "Constraints validadas"


    def get_registro(self, indice):
        node = self.buscar_node(int(indice))
        if not node:
            return None, node
        
        dados_brutos = self._gerenciador_txt.acessar(node.get_offs())
        dados = dados_brutos.strip().split(";")
        registro = RegistroLicoes(dados[0], dados[1], dados[2])

        return registro

    def listar_registros(self):
    
        lista_registros = []
        lista_dados = self.listar_dados()

        for i in range(len(lista_dados)):
            lista_registros.append(RegistroLicoes(lista_dados[i][0], lista_dados[i][1], lista_dados[i][2]))

        return lista_registros