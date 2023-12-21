 ## **README.md**

### **Descrição**

Este código em Python é uma aplicação simples para gerenciar contas financeiras, incluindo contas de crédito, conta corrente e conta poupança. Ele permite registrar despesas, recebimentos, exportar/importar extratos e consultar faturas.

### **Requisitos** 
- Bibliotecas necessárias: numpy, matplotlib, pandas, openpyxl

### **Estrutura do Código**
O código está dividido em três classes principais:

- Conta: Classe base que armazena informações comuns a todas as contas (nome do titular, nome do banco, etc.).

- Credito (Conta): Classe que representa uma conta de crédito. Permite registrar gastos, calcular faturas, exportar/importar faturas em formato CSV.

- ContaCorrente (Conta): Classe que representa uma conta corrente. Permite registrar recebimentos, gastos, exportar/importar extratos em formato CSV.

- ContaPoupanca (Conta): Classe que representa uma conta poupança. Permite exibir um resumo do rendimento.

### **Funcionalidades** 
**Classe Conta**
- Método resumo(): Exibe um resumo das informações da conta.
**Classe Credito**
- Método resumo(): Exibe um resumo da conta de crédito.
- Método gasto(data, descr, valor, parcela=1): Registra uma despesa na conta de - crédito, permitindo parcelamento.
- Método exportar_fatura(path=None): Exporta a fatura da conta de crédito para um arquivo CSV.
- Método consultar_fatura(path=None): Consulta a fatura da conta de crédito a partir de um arquivo CSV.
**Classe ContaCorrente**
- Método recebimento(data, desc, valor): Registra um recebimento na conta corrente.
- Método gasto(data, desc, valor): Registra um gasto na conta corrente.
- Método exportar_extrato(path=None): Exporta o extrato da conta corrente para um arquivo CSV.
- Método consultar_extrato(path=None): Consulta o extrato da conta corrente a partir de um arquivo CSV.
**Classe ContaPoupanca**
- Método resumo(): Exibe um resumo da conta poupança.

### **Exemplos de uso**

```
# Exemplo de uso para uma conta de crédito (NuBank)
nu_cred = Credito('Rafael', 'NuBank', 5000, '18/12/2023', '26/12/2023')
nu_cred.gasto('10/12/2023', 'Compras de Natal', 300)
nu_cred.exportar_fatura()
nu_cred.consultar_fatura()

# Exemplo de uso para uma conta corrente (NuBank)
nu_deb = ContaCorrente('Rafael', 'NuBank')
nu_deb.recebimento('1/1/2024', 'Pix', 500)
nu_deb.gasto('2/1/2024', 'Padaria', 30)
nu_deb.exportar_extrato()
nu_deb.consultar_extrato()

# Exemplo de uso para uma conta poupança
conta_poupanca = ContaPoupanca('João', 1000, 0.5)
conta_poupanca.resumo()
```

# Autores
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/37356058?v=4" width=115><br><sub>Camila Fernanda Alves</sub>](https://github.com/camilafernanda) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/30351153?v=4" width=115><br><sub>Guilherme Lima</sub>](https://github.com/guilhermeonrails) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/8989346?v=4" width=115><br><sub>Alex Felipe</sub>](https://github.com/alexfelipe) |
| :---: | :---: | :---: |
