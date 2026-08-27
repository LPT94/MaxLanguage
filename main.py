from Estruturas.Gerenciador_txt import GerenciadorTxt
from Estruturas.Nodes import Node
from Estruturas.Arvore_indices import ArvoreB


N = Node(50, 231)
T = ArvoreB(N)
T.inserir_node(Node(25,121))
x = T.deletar_node(50)
T.print_in_order(T.root)