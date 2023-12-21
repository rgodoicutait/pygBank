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

# Restante do seu código...

# Atualização da função clique para usar a verificação de credenciais
def clique():
    if verificar_credenciais(email.get(), senha.get()):
        fazer_login()
    else:
        print("Credenciais inválidas")