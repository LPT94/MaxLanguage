from Estruturas.Controlador import Controlador
from Estruturas.RegistroUsuarios import RegistroUsuarios
import hashlib

class ControladorUsuarios(Controlador):

    def __init__(self, nome_arquivo, controlador_idiomas):
        super().__init__(nome_arquivo)
        self._controlador_idiomas = controlador_idiomas

    def validar_constraints(self, registro):
    
        no_estrangeiro = self._controlador_idiomas.buscar_node(registro.get_cod_idioma())
        if not no_estrangeiro:
            print("Erro! Foreign Key não encontrada na tabela lições.")
            return False

        if not self.unique(registro.get_login(), 3):
            print("Erro! Atributo login deve ser único")
            return False

        return True

    def get_registro(self, indice):

        node = self.buscar_node(indice)
        if not node:
            return None, node
        
        dados_brutos = self._gerenciador_txt.acessar(node.get_offs())
        dados = dados_brutos.strip().split(";")
        registro = RegistroUsuarios(dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], 
                                        dados[6], dados[7])

        return registro, node

    def autenticar(self, login, senha):
        senha = hashlib.sha256(senha.encode("utf-8")).hexdigest()
        lista_elements = self.pegar_registro_criterio({3: login, 4: senha})
        if not lista_elements:
            return None

        return RegistroUsuarios(lista_elements[0][0], lista_elements[0][1], lista_elements[0][2], lista_elements[0][3],
                                    lista_elements[0][4], lista_elements[0][5], lista_elements[0][6], lista_elements[0][7])
            
        
