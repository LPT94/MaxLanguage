import flet as ft
from Views.usuario import usuario_view
from Views.cadastro import cadastro_view

def login_view(page: ft.Page):

    #função que direciona para página do usuário
    def clicou_login(e):
        print("login : ", login.value, "\nsenha: ", senha.value)
        page.clean()
        usuario_view(page)

    #função que direciona para página de cadastro
    def clicou_cadastro(e):
        print("Clicou cadastrar! ")
        page.clean()
        cadastro_view(page)

    #criando os controlers separadamente
    login = ft.TextField(
        label="Login"
    )

    senha = ft.TextField(
        label="Senha",
        password=True
    )

    botao_login = ft.ElevatedButton(
        "Entrar", on_click=clicou_login
    )

    botao_cadastro = ft.ElevatedButton(
        "Criar registro", on_click=clicou_cadastro
    )

    #criando um agrupamento horizontal de controlers
    botoes = ft.Row(
        controls=[
            botao_login,
            botao_cadastro
        ],
        alignment=ft.MainAxisAlignment.CENTER                       # Centraliza no eixo horizontal
    )

    #criando um agrupamento vertical de controlers
    coluna = ft.Column(
        controls=[
            login,
            senha,
            botoes
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER           #Centraliza no eixo vertical
    )

    #criando um agrupamento de container dos agrupamentos dos controlers
    container = ft.Container(
        content=coluna,
        alignment=ft.Alignment.CENTER                               #centraliza todo o container (bloco)
    )

    #adicionando na página
    page.add(
        container
    )

