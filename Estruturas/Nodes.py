class Node:
    def __init__(self, indice, offset):
        self.__indice = indice
        self.__offset = offset
        self.__esquerda = None
        self.__direita = None

    def get_i(self):
        return self.__indice

    def get_offs(self):
        return self.__offset

    def get_e(self):
        return self.__esquerda

    def get_d(self):
        return self.__direita

    def set_e(self, Node):
        self.__esquerda = Node

    def set_d(self, Node):
        self.__direita = Node

    def set_i(self, indice):
        self.__indice = indice

    def set_off(self, offset):
        self.__offset = offset