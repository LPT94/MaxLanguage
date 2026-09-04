class RegistroExerciciosFeitos:

    def __init__(self, cod_usuario, cod_exercicios):
        self._id = cod_usuario*10000 + cod_exercicios
        self._cod_usuario = cod_usuario
        self._cod_exercicio = cod_exercicios

    def get_id(self):
        return int(self._id)

    def get_cod_usuario(self):
        return int(self._cod_usuario)

    def get_cod_exercicio(self):
        return int(self._cod_exercicio)

    def formatar(self):
        return str(self._id)+";"+str(self._cod_usuario)+";"+str(self._cod_exercicio)
        