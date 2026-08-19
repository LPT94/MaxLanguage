files = ["idiomas.txt", "licoes.txt", "exercicios.txt", "usuarios.txt"]


for i in range(len(files)):
    try:
        with open("Tabelas/" + files[i], "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            print(conteudo)

    except FileNotFoundError:
        print("Arquivo não encontrado.")

