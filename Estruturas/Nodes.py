class Node:
    def __init__(self, indice, offset):
        self._indice = indice
        self._offset = offset
        self._esquerda = None
        self._direita = None

    def get_i(self):
        return self._indice

    def get_offs(self):
        return self._offset

    def get_e(self):
        return self._esquerda

    def get_d(self):
        return self._direita

    def set_e(self, Node):
        self._esquerda = Node

    def set_d(self, Node):
        self._direita = Node

    def set_i(self, indice):
        self._indice = indice

    def set_off(self, offset):
        self._offset = offset