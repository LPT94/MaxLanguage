from Controllers.Controlador import Controlador
from Registers.RegistroExerciciosFeitos import RegistroExerciciosFeitos

class ControladorExerciciosFeitos(Controlador):

    def __init__(self, nome_arquivo, controlador_usuarios, controlador_exercicios):
        super().__init__(nome_arquivo)
        self._controlador_usuarios = controlador_usuarios
        self._controlador_exercicios = controlador_exercicios

    def validar_dados(self, registro):

        cod_usuario = registro.get_cod_usuario()
        cod_exercicio = registro.get_cod_exercicio()
        if not self._eh_int([cod_usuario, cod_exercicio],
                            ['codigo usuario', 'codigo exercicio']):
            return False

        registro.set_id(int(cod_usuario), int(cod_exercicio))
        return True
    
    def validar_constraints(self, registro):

        no_estrangeiro_user = self._controlador_usuarios.buscar_node(int(registro.get_cod_usuario()))
        if not no_estrangeiro_user:
            print("Erro! Foreign Key não encontrada na tabela usuarios.")
            return False

        no_estrangeiro_exe = self._controlador_exercicios.buscar_node(int(registro.get_cod_exercicio()))
        if not no_estrangeiro_exe:
            print("Erro! Foreign Key não encontrada na tabela exercicios.")
            return False

        return True

    def get_registro(self, indice):

        node = self.buscar_node(indice)
        if not node:
            return None, node
        
        dados_brutos = self._gerenciador_txt.acessar(node.get_offs())
        dados = dados_brutos.strip().split(";")
        registro = RegistroExerciciosFeitos(dados[0], dados[1], dados[2])

        return registro, node