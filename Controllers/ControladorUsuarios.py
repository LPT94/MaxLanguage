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

        no_estrangeiro = self._controlador_idiomas.buscar_node(int(registro.get_cod_idioma()))
        if not no_estrangeiro:
            return False, "Idioma selecionado não encontrado."
        
        return True, "Dados válidos."


    def validar_constraints_insert(self, registro):
        if not self.unique(registro.get_login(), 3):
            return False, "Login já existente."

        return True, "Constraints validadas."

    def validar_constraints_edit(self, registro, controlador=None):
        return True, "Constraints validadas."


    def __procurar_e_deletar(self, arquivo, node, valor, ctrl_exe_feitos):
            if node is None:
                return
    
            arquivo.seek(node.get_offs())
            dados = arquivo.readline().strip().split(";")
            if dados[1] == str(valor):
                ctrl_exe_feitos.del_registro(dados[0], [])
    
            self.__procurar_e_deletar(arquivo, node.get_e(), valor, ctrl_exe_feitos)
            self.__procurar_e_deletar(arquivo, node.get_d(), valor, ctrl_exe_feitos)
            
    
    def validar_cascade(self, lista_info):
        arquivo = open(lista_info[0].get_nome_arq(), "r", encoding="utf-8")
        self.__procurar_e_deletar(arquivo, lista_info[0]._arvore_indices.get_root(), lista_info[1], lista_info[0])
        arquivo.close()
        return True, "Constraints validadas."
    

    def get_registro(self, indice):
        #TODO: VERIFICAR SE RETORNAR NODE É REALMENTE NECESSÁRIO
        node = self.buscar_node(int(indice))
        if not node:
            return None
        
        dados_brutos = self._gerenciador_txt.acessar(node.get_offs())
        dados = dados_brutos.strip().split(";")
        registro = RegistroUsuarios(dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], 
                                    dados[6], dados[7])
        return registro


    def autenticar(self, login, senha):
        senha = hashlib.sha256(senha.encode("utf-8")).hexdigest()
        lista_elements = self.registros_com_criterio({3: login, 4: senha})
        if not lista_elements:
            return None

        return RegistroUsuarios(lista_elements[0][0], lista_elements[0][1], lista_elements[0][2], lista_elements[0][3],
                                    lista_elements[0][4], lista_elements[0][5], lista_elements[0][6], lista_elements[0][7])
            
        
