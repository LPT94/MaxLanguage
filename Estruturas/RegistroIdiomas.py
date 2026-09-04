class RegistroIdiomas:

    def __init__(self, codigo, descricao):
        self._id = codigo
        self._descricao = descricao

    def get_id(self):
        return int(self._id)

    def get_descricao(self):
        return int(self._descricao)

    def set_descricao(self, descricao):
        self._descricao = descricao

    def formatar(self):
        return str(self._id)+";"+str(self._descricao)
        