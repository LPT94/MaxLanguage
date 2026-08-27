from Estruturas.Nodes import Node

class ArvoreB:

    def __init__(self, node):
        self.root = node

    def atualiza_root(self, node):
        self.root = node

    def buscar_node(self, indice):

        Node = self.root
        Pai = None

        while Node and Node.get_i() != indice:
            Pai = Node
            if indice > Node.get_i():
                Node = Node.get_d()

            else:
                Node = Node.get_e()

        return Node, Pai

    def inserir_node(self, Node):
        if not self.root:
            self.root = Node
            return True
        
        busca = self.buscar_node(Node.get_i())
        if busca[0]:
            print("Erro! Indice já existente")
            return False

        if Node.get_i() > busca[1].get_i():
            busca[1].set_d(Node)
        else:
            busca[1].set_e(Node)

        return True
        
    def print_in_order(self, Node):
        if not Node:
            return

        self.print_in_order(Node.get_e())
        print(Node.get_i(), end=" ")
        self.print_in_order(Node.get_d())

        

    
