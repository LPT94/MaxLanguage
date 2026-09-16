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

        validacao, mensagem = self._eh_int([cod_usuario, cod_exercicio],
                            ['codigo usuario', 'codigo exercicio'])
        if not validacao:
            return validacao, mensagem
        
        no_estrangeiro_user = self._controlador_usuarios.buscar_node(int(registro.get_cod_usuario()))
        if not no_estrangeiro_user:
            return False, "Usuário não encontrado."

        no_estrangeiro_exe = self._controlador_exercicios.buscar_node(int(registro.get_cod_exercicio()))
        if not no_estrangeiro_exe:
            return False, "Exercício não encontrado"

        registro.set_id(int(cod_usuario), int(cod_exercicio))
        return True, "Dados validados."

    
    def validar_constraints_edit(self, registro):
        node = self.buscar_node(int(registro.get_id()))
        if node:
            return False, "Id já cadastrado"
        
        return True, "Constraints validadas"


    def validar_constraints_edit(self, registro, controlador=None):
        existe = self.buscar_node(int(registro.get_id()))
        if existe:
            return False, "Exercício feito já está cadastrado."

        return True, "Constraints validadas."

    def validar_cascade(self, lista_referencia):
        return True, "Constraints validadas"


    def get_registro(self, indice):
        node = self.buscar_node(int(indice))
        if not node:
            return None
        
        dados_brutos = self._gerenciador_txt.acessar(node.get_offs())
        dados = dados_brutos.strip().split(";")
        registro = RegistroExerciciosFeitos(dados[0], dados[1], dados[2])

        return registro