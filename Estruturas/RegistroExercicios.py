class RegistroExercicios:

    def __init__(self, id, cod_licao, nivel, descricao, opcao_a, opcao_b, 
                 opcao_c, opcao_d, opcao_correta, pontuacao):
        self.__id = id
        self.__cod_licao = cod_licao
        self.__nivel = nivel
        self.__descricao = descricao
        self.__a = opcao_a
        self.__b = opcao_b
        self.__c = opcao_c
        self.__d = opcao_d
        self.__opcao_correta = opcao_correta
        self.__pontuacao = pontuacao

    def get_id(self):
        return self.__id

    def get_licao(self):
        return self.__cod_licao

    def get_nivel(self):
        return self.__nivel

    def get_descricao(self):
        return self.__descricao

    def get_op_a(self):
        return self.__a

    def get_op_b(self):
        return self.__b

    def get_op_c(self):
        return self.__c

    def get_op_d(self):
        return self.__d

    def get_op_correta(self):
        return self.__opcao_correta

    def get_pontuacao(self):
        return self.__pontuacao

    def get_reg_editado(self):
        reg = str(self.__id)+";"+str(self.__cod_licao)+";"+str(self.__nivel)+";"+str(self.__descricao)+";"+str(self.__a)+";"+str(self.__b)+";"+str(self.__c)+";"+str(self.__d)+";"+str(self.__opcao_correta)+";"+str(self.__pontuacao)
        return reg


    