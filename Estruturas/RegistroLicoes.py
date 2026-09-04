class RegistroLicoes:

    def __init__(self, id, cod_idioma, total_niveis):
        self._id = id
        self._cod_idioma = cod_idioma
        self._total_niveis = total_niveis

    def get_id(self):
        return self._id

    def get_cod_idioma(self):
        return self._cod_idioma

    def get_total_niveis(self):
        return int(self._total_niveis)

    def formatar(self):
        return str(self._id)+";"+str(self._cod_idioma)+";"+str(self._total_niveis)