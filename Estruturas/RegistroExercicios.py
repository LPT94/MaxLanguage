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
        return self._id

    def get_licao(self):
        return self._cod_licao

    def get_nivel(self):
        return self._nivel

    def get_descricao(self):
        return self._descricao

    def get_op_a(self):
        return self._a

    def get_op_b(self):
        return self._b

    def get_op_c(self):
        return self._c

    def get_op_d(self):
        return self._d

    def get_op_correta(self):
        return self._opcao_correta

    def get_pontuacao(self):
        return self._pontuacao

    def formatar(self):
        reg = str(self._id)+";"+str(self._cod_licao)+";"+str(self._nivel)+";"+str(self._descricao)+";"+str(self._a)+";"+str(self._b)+";"+str(self._c)+";"+str(self._d)+";"+str(self._opcao_correta)+";"+str(self._pontuacao)
        return reg


    