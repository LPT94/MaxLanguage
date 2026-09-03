from Estruturas.Nodes import Node

class ArvoreB:

    def __init__(self, node):
        self._root = node

    def get_root(self):
        return self._root

    def atualiza_root(self, node):
        self._root = node

    def filho_esq(self, node_filho, node_pai):

        if node_filho.get_i() < node_pai.get_i():
            return True

        return False

    def filho_dir(self, node_filho, node_pai):

        if node_filho.get_i() > node_pai.get_i():
            return True

        return False

    def tio(self, node_pai, node_avo):

        if self.filho_esq(node_pai, node_avo) and node_avo.get_d() != None:
            return True

        elif self.filho_dir(node_pai, node_avo) and node_avo.get_e() != None:
            return True

        return False

    def buscar(self, indice):

        node = self._root
        pai = None

        while node and node.get_i() != indice:
            pai = node
            if indice > node.get_i():
                node = node.get_d()

            else:
                node = node.get_e()

        return node, pai

    def inserir(self, node):
        if not self._root:
            self._root = node
            return True
        
        existe, pai = self.buscar(node.get_i())
        if existe:
            print("Erro! Indice já existente")
            return False

        if node.get_i() > pai.get_i():
            pai.set_d(node)
        else:
            pai.set_e(node)

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

    def deletar(self, indice):

        del_node, pai_master = self.buscar(indice)

        if not del_node:
            print("Erro! indice não encontrado.")
            return del_node

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

        return del_node

        
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

    def print_in_width(self):
        fila = []
        if self._root:
            fila.append(self._root)

        else:
            print("Arvore vazia")

        i = 1
        j = 1

        while(fila):
            node = fila.pop(0)
            print(node.get_i(), end = " ")
            if(node.get_e()):
                fila.append(node.get_e())
            if(node.get_d()):
                fila.append(node.get_d())
            if 2**j-1 == i:
                print()
                j += 1
            i += 1

                   
    def balancear(self, node, pai):

        pai, avo = self.buscar(pai)

        if not self.tio(pai, avo):
            self.deletar_node(avo)
            avo.set_e(None)
            avo.set_d(None)
            self.inserir_node(avo)

        else:
            avo, bisavo = self.buscar(avo)
            self.deletar_node(pai)
            pai.set_e(None)
            pai.set_d(None)
            self.inserir_node(pai)
            #substitui Node - Avo
            if self.filho_dir(node, avo):
                node.set_e(avo)
                avo.set_d(None)
            else:
                node.set_d(avo)
                avo.set_e(None)

            if bisavo:
                if self.filho_dir(avo, bisavo):
                    bisavo.set_d(node)
                else:
                    bisavo.set_e(Node)



    
