import customtkinter as ctk
import pandas as pd

# Função para verificar as credenciais do usuário
def verificar_credenciais(username, password):
    # Carregar os dados do arquivo Excel (substitua 'caminho/do/arquivo.xlsx' pelo seu caminho)
    dados_usuarios = pd.read_excel('usuarios.xlsx')
    
    # Verificar se o usuário e a senha estão na lista carregada do Excel
    if (dados_usuarios['Email'] == username).any() and (dados_usuarios['senha'] == password).any():
        return True
    else:
        return False


# Atualização da função clique para usar a verificação de credenciais
def clique():
    if verificar_credenciais(email.get(), senha.get()):
        fazer_login()
    else:
        print("Credenciais inválidas")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def fazer_login():
    # Aqui você pode adicionar a lógica para verificar as credenciais de login
    # Se o login for bem-sucedido, abra uma nova janela para as opções do banco
    nova_janela = ctk.CTk()
    nova_janela.geometry("500x300")

    def selecionar_banco(banco):
        print(f"Banco selecionado: {banco}")

    label_opcoes = ctk.CTkLabel(nova_janela, text="Selecione o Banco")
    label_opcoes.pack(padx=10, pady=10)

    # Adicione botões para os bancos disponíveis
    bancos = ["Visão Geral", "Banco do Brasil", "Nubank", "Itaú"]  # Adicione os nomes dos bancos aqui
    for banco in bancos:
        botao_banco = ctk.CTkButton(nova_janela, text=banco, command=lambda b=banco: selecionar_banco(b))
        botao_banco.pack(padx=10, pady=5)

    nova_janela.mainloop()

def clique():
    # Verificar o login aqui, por exemplo:
    # if verificar_credenciais(email.get(), senha.get()):
    #     fazer_login()
    fazer_login()

janela = ctk.CTk()
janela.geometry("500x300")

texto = ctk.CTkLabel(janela, text="Fazer Login")
email = ctk.CTkEntry(janela, placeholder_text="E-mail")
senha = ctk.CTkEntry(janela, placeholder_text="Senha", show="*")
botao = ctk.CTkButton(janela, text="Login", command=clique)

texto.pack(padx=10, pady=10)
email.pack(padx=10, pady=10)
senha.pack(padx=10, pady=10)
botao.pack(padx=10, pady=10)

janela.mainloop()
