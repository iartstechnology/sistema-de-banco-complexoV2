class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

    def __str__(self):
        return f"Nome: {self.nome}, CPF: {self.cpf}, Endereço: {self.endereco}"


class ContaCorrente:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.depositos = []
        self.saques = []
        self.saques_diarios = 0

    def __str__(self):
        return f"Agência: {self.agencia}, Número da Conta: {self.numero_conta}, Usuário: {self.usuario.nome}"


class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.conta_atual = None

    def cadastrar_usuario(self, nome, data_nascimento, cpf, endereco):
        if cpf in [u.cpf for u in self.usuarios]:
            print("Erro: CPF já cadastrado.")
            return
        usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(usuario)
        print(f"Usuário {nome} cadastrado com sucesso!")

    def criar_conta_corrente(self, cpf):
        usuario = self.buscar_usuario_por_cpf(cpf)
        if not usuario:
            print("Erro: Usuário não encontrado.")
            return
        numero_conta = len(self.contas) + 1
        conta = ContaCorrente("0001", numero_conta, usuario)
        self.contas.append(conta)
        print(f"Conta corrente criada com sucesso! Número da Conta: {numero_conta}")

    def buscar_usuario_por_cpf(self, cpf):
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def deposito(self, valor):
        if valor <= 0:
            print("Erro: Valor de depósito inválido. Somente valores positivos são permitidos.")
            return
        if self.conta_atual:
            self.conta_atual.saldo += valor
            self.conta_atual.depositos.append(f"Depósito de R${valor:.2f}")
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
        else:
            print("Erro: Nenhuma conta selecionada.")

    def saque(self, valor):
        if valor <= 0:
            print("Erro: Valor de saque inválido. Somente valores positivos são permitidos.")
            return
        if self.conta_atual:
            if self.conta_atual.saldo < valor:
                print("Erro: Saldo insuficiente. Não é possível sacar o dinheiro.")
                return
            if self.conta_atual.saques_diarios >= 3:
                print("Erro: Limite de saques diários atingido. Tente novamente amanhã.")
                return
            self.conta_atual.saldo -= valor
            self.conta_atual.saques.append(f"Saque de R${valor:.2f}")
            self.conta_atual.saques_diarios += 1
            print(f"Saque de R${valor:.2f} realizado com sucesso!")
        else:
            print("Erro: Nenhuma conta selecionada.")

    def extrato(self, detalhes=False, mostrar_saldo=True):
        if self.conta_atual:
            print("Extrato da conta:")
            for deposito in self.conta_atual.depositos:
                print(deposito)
            for saque in self.conta_atual.saques:
                print(saque)
            if mostrar_saldo:
                print(f"Saldo atual: R${self.conta_atual.saldo:.2f}")
            if detalhes:
                print(f"Usuário: {self.conta_atual.usuario.nome}")
                print(f"Agência: {self.conta_atual.agencia}, Número da Conta: {self.conta_atual.numero_conta}")
        else:
            print("Erro: Nenhuma conta selecionada.")

    def listar_contas(self):
        for conta in self.contas:
            print(conta)

    def selecionar_conta(self, numero_conta):
        for conta in self.contas:
            if conta.numero_conta == numero_conta:
                self.conta_atual = conta
                print(f"Conta {numero_conta} selecionada com sucesso!")
                return
        print("Erro: Conta não encontrada.")


banco = Banco()

while True:
    print("Opções:")
    print("1. Cadastrar usuário")
    print("2. Criar conta corrente")
    print("3. Selecionar conta")
    print("4. Depósito")
    print("5. Saque")
    print("6. Extrato")
    print("7. Listar contas")
    print("8. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Digite o nome do usuário: ")
        data_nascimento = input("Digite a data de nascimento do usuário (formato dd/mm/aaaa): ")
        cpf = input("Digite o CPF do usuário (somente os números): ")
        endereco = input("Digite o endereço do usuário (formato logradouro, número - bairro - cidade/sigla estado): ")
        banco.cadastrar_usuario(nome, data_nascimento, cpf, endereco)
    elif opcao == "2":
        cpf = input("Digite o CPF do usuário que vai cadastrar a conta corrente: ")
        banco.criar_conta_corrente(cpf)
    elif opcao == "3":
        numero_conta = int(input("Digite o número da conta que deseja selecionar: "))
        banco.selecionar_conta(numero_conta)
    elif opcao == "4":
        valor = float(input("Digite o valor do depósito: "))
        banco.deposito(valor)
    elif opcao == "5":
        valor = float(input("Digite o valor do saque: "))
        banco.saque(valor)
    elif opcao == "6":
        detalhes = input("Deseja ver detalhes do extrato (s/n)? ").lower() == "s"
        mostrar_saldo = input("Deseja ver o saldo (s/n)? ").lower() == "s"
        banco.extrato(detalhes, mostrar_saldo=mostrar_saldo)
    elif opcao == "7":
        banco.listar_contas()
    elif opcao == "8":
        print("Obrigado por usar o sistema!")
        break
    else:
        print("Opção inválida. Tente novamente.")
