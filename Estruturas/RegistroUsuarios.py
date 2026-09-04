class RegistroUsuarios:

    def __init__(self, id, cod_idioma, nome, login, senha, nivel_atual, pontuacao_total, tipo):
        self._id = id
        self._cod_idioma = cod_idioma
        self._nome = nome
        self._login = login
        self._senha = senha
        self._nivel_atual = nivel_atual
        self._pontuacao = pontuacao_total
        self._tipo = tipo                           #tipo: 0 ->admin || 1->usuario comum

    def get_id(self):
        return int(self._id)

    def get_cod_idioma(self):
        return int(self._cod_idioma)

    def get_nome(self):
        return str(self._nome)

    def get_login(self):
        return str(self._login)

    def get_senha(self):
        return str(self._senha)

    def get_nivel_atual(self):
        return int(self._nivel_atual)

    def get_pontuacao(self):
        return int(self._pontuacao)

    def get_tipo(self):
        return str(self._tipo)

    def formatar(self):
            return str(self._id)+";"+str(self._cod_idioma)+";"+str(self._nome)+";"+str(self._login)+";"+str(self._senha)+";"+str(self._nivel_atual)+";"+str(self._pontuacao)+";"+str(self._tipo)