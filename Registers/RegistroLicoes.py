class RegistroLicoes:

    def __init__(self, id, cod_idioma, total_niveis, descricao):
        self._id = id
        self._cod_idioma = cod_idioma
        self._total_niveis = total_niveis
        self._descricao = descricao

    def get_id(self):
        return self._id

    def get_cod_idioma(self):
        return self._cod_idioma

    def get_total_niveis(self):
        return self._total_niveis

    def get_descricao(self):
        return self._descricao

    def set_cod_idioma(self, cod_idioma):
        self._cod_idioma = cod_idioma

    def set_total_niveis(self, total_niveis):
        self._total_niveis = total_niveis

    def formatar(self):
        return str(self._id)+";"+str(self._cod_idioma)+";"+str(self._total_niveis)+";"+str(self._descricao)