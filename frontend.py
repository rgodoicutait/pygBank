import customtkinter as ctk
#from pygBank import Conta, ContaCorrente, ContaPoupanca, Credito
#path = r"C:\Users\Usuário\OneDrive\pygBank\pygBank\bancodedados.csv"
#nu_cred = Credito("Rafael","NuBank",100,3000,"18/12/2023","26/12/2023",db_path=path)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

janela = ctk.CTk()
janela.geometry("500x300")

def clique():
    print("Fazer Login")

texto = ctk.CTkLabel(janela, text="Fazer Login")

email = ctk.CTkEntry(janela,
                     placeholder_text="E-mail")

senha = ctk.CTkEntry(janela,
                     placeholder_text="senha",
                     show="*")
botao = ctk.CTkButton(janela, text="Login",
                      command=clique)

texto.pack(padx=10, pady=10)
email.pack(padx=10, pady=10)
senha.pack(padx=10, pady=10)
botao.pack(padx=10, pady=10)


janela.mainloop()