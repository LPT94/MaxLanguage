class RegistroExercicios:

    def __init__(self, id, cod_licao, nivel, descricao, opcao_a, opcao_b, 
                 opcao_c, opcao_d, opcao_correta, pontuacao):
        self._id = id
        self._cod_licao = cod_licao
        self._nivel = nivel
        self._descricao = descricao
        self._a = opcao_a
        self._b = opcao_b
        self._c = opcao_c
        self._d = opcao_d
        self._opcao_correta = opcao_correta
        self._pontuacao = pontuacao

    def get_id(self):
        return int(self._id)

    def get_licao(self):
        return int(self._cod_licao)

    def get_nivel(self):
        return int(self._nivel)

    def get_descricao(self):
        return str(self._descricao)

    def get_op_a(self):
        return str(self._a)

    def get_op_b(self):
        return str(self._b)

    def get_op_c(self):
        return str(self._c)

    def get_op_d(self):
        return str(self._d)

    def get_op_correta(self):
        return int(self._opcao_correta)

    def get_pontuacao(self):
        return int(self._pontuacao)

    def set_licao(self, licao):
        self._cod_licao = licao

    def set_nivel(self, nivel):
        self._nivel = nivel

    def set_descricao(self, descricao):
        self._descricao = descricao

    def set_op_a(self, op_a):
        self._a = op_a

    def set_op_b(self, op_b):
        self._b = op_b

    def set_op_c(self, op_c):
        self._c = op_c

    def set_op_d(self, op_d):
        self._d = op_d

    def set_op_correta(self, op_correta):
        self._opcao_correta = op_correta

    def set_pontuacao(self, potuacao):
        self._pontuacao = potuacao

    def formatar(self):
        reg = str(self._id)+";"+str(self._cod_licao)+";"+str(self._nivel)+";"+str(self._descricao)+";"+str(self._a)+";"+str(self._b)+";"+str(self._c)+";"+str(self._d)+";"+str(self._opcao_correta)+";"+str(self._pontuacao)
        return reg


    