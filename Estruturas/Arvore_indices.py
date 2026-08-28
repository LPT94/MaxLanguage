from Estruturas.Nodes import Node

class ArvoreB:

    def __init__(self, node):
        self.root = node

    def atualiza_root(self, node):
        self.root = node

    def filho_esq(self, node_filho, node_pai):

        if node_filho.get_i() < node_pai.get_i():
            return True

        return False

    def filho_dir(self, node_filho, node_pai):

        if node_filho.get_i() > node_pai.get_i():
            return True

        return False

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

    def inserir_node(self, node):

        if not self.root:
            self.root = node
            return True
        
        busca = self.buscar_node(node.get_i())
        if busca[0]:
            print("Erro! Indice já existente")
            return False

        if node.get_i() > busca[1].get_i():
            busca[1].set_d(node)
        else:
            busca[1].set_e(node)

        return True

    def buscar_subst_esq(self, node):

        sub = node.get_e()
        pai_sub = None

        while sub.get_d():
            pai_sub = sub
            sub = sub.get_d()

        return sub, pai_sub

    def buscar_subst_dir(self, node):

        sub = node.get_d()
        pai_sub = None

        while sub.get_e():
            pai_sub = sub
            sub = sub.get_e()

        return sub, pai_sub   

    def deletar_node(self, indice):

        del_node, pai_master = self.buscar_node(indice)

        if not del_node:
            print("Erro! indice não encontrado.")
            return False

        if del_node.get_e():
            sub, pai_sub = self.buscar_subst_esq(del_node)
            if pai_sub:
                pai_sub.set_d(sub.get_e())
                sub.set_e(del_node.get_e())

            sub.set_d(del_node.get_d())

        elif del_node.get_d():
            sub, pai_sub = self.buscar_subst_dir(del_node)
            if pai_sub:
                pai_sub.set_e(sub.get_d())
                sub.set_d(del_node.get_d())

            sub.set_e(del_node.get_e())

        else:
            sub = None

        if pai_master:
            if self.filho_esq(del_node, pai_master):
                pai_master.set_e(sub)
            else:
                pai_master.set_d(sub)
        else:
            self.root = sub

        return True

        
    def print_pre_order(self, node):

        if not node:
            return

        self.print_pre_order(node.get_e())
        print(node.get_i(), end=" ")
        self.print_pre_order(node.get_d())

    def print_in_order(self, node):

        if not node:
            return

        print(node.get_i(), end=" ")
        self.print_in_order(node.get_e())
        self.print_in_order(node.get_d())
        

    
