from Controllers.Controlador import Controlador
from Registers.RegistroUsuarios import RegistroUsuarios
import hashlib

class ControladorUsuarios(Controlador):

    def __init__(self, nome_arquivo, controlador_idiomas):
        super().__init__(nome_arquivo)
        self._controlador_idiomas = controlador_idiomas

    def validar_dados(self, registro):

        tipo = registro.get_tipo()
        nivel_atual = registro.get_nivel_atual()
        pontuacao = registro.get_pontuacao()

        verificacao, mensagem = self._eh_int([registro.get_id(), registro.get_cod_idioma(),nivel_atual,
                            pontuacao], ['Id', 'Código Idioma', 'Nivel Atual', 'Pontuação'])
        if not verificacao:
            return verificacao, mensagem

        verificacao, mensagem = self._caracter_valido([registro.get_nome(), registro.get_login(), registro.get_tipo()], 
                                     ['Nome', 'Login', 'Tipo'])
        if not verificacao:
            return verificacao, mensagem

        if str(tipo) != "0" and str(tipo) != "1":
            return False, "Tipo deve ser 0 ou 1."

        if int(nivel_atual) < 1:
            return False, "Nivel atual deve ser maior ou igual a 1."

        if int(pontuacao) < 0:
            return False, "Pontuação deve ser maior que 0."
        
        return True, "Dados válidos."

    def validar_constraints(self, registro):

        no_estrangeiro = self._controlador_idiomas.buscar_node(int(registro.get_cod_idioma()))
        if not no_estrangeiro:
            return False, "Idioma selecionado não encontrado."

        if not self.unique(registro.get_login(), 3):
            return False, "Login já existente."

        return True, "Constraints válidadas."

    def get_registro(self, indice):

        #TODO: VERIFICAR SE RETORNAR NODE É REALMENTE NECESSÁRIO

        node = self.buscar_node(int(indice))
        if not node:
            return None, node
        
        dados_brutos = self._gerenciador_txt.acessar(node.get_offs())
        dados = dados_brutos.strip().split(";")
        registro = RegistroUsuarios(dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], 
                                        dados[6], dados[7])

        return registro, node

    def autenticar(self, login, senha):
        senha = hashlib.sha256(senha.encode("utf-8")).hexdigest()
        lista_elements = self.registros_com_criterio({3: login, 4: senha})
        if not lista_elements:
            return None

        return RegistroUsuarios(lista_elements[0][0], lista_elements[0][1], lista_elements[0][2], lista_elements[0][3],
                                    lista_elements[0][4], lista_elements[0][5], lista_elements[0][6], lista_elements[0][7])
            
        
