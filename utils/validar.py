def ler_int(mensagem, permitir_cancelar=True):
    # Lê um número inteiro com tratamento de erros.
    while True:
        try:
            valor = input(mensagem).strip()
            # Verificar cancelamento ("c ou C").
            if permitir_cancelar and valor.lower() == "c":
                print("Operação cancelada. Voltando ao menu principal.")
                return None
            return int(valor)
        except ValueError:
            print("Entrada inválida. Por favor, digite um número válido ou 'C' para cancelar.")

def ler_float(mensagem, permitir_cancelar=True):
    # Lê um número de ponto flutuante com tratamento de erros.
    while True:
        try:
            valor = input(mensagem).strip()
            # Verificar cancelamento ("c ou C").
            if permitir_cancelar and valor.lower() == "c":
                print("Operação cancelada. Voltando ao menu principal.")
                return None
            return float(valor)
        except ValueError:
            print("Entrada inválida. Por favor, digite um número válido ou 'C' para cancelar.")

def ler_string(mensagem, obrigatorio=True, permitir_cancelar=True):
    # Lê string com validação.
    while True:
        valor = input(mensagem).strip()
        # Verificar cancelamento ("c ou C").
        if permitir_cancelar and valor.lower() == "c":
            print("Operação cancelada. Voltando ao menu principal.")
            return None
        if not obrigatorio or valor:
            return valor
        print("Entrada obrigatória. Por favor, digite um valor ou 'C' para cancelar.")

def ler_sim_nao(mensagem="Confirmação? (S/N): ")
    while True:
        valor = input(mensagem).strip().lower()
        # cancelamento.
        if valor == "c":
            print("Operação cancelada. Voltando ao menu principal.")
            return None
        # Sim.
        if valor in ["s", "sim"]:
            return True
        # Não.
        if valor in ["n", "não", "nao", ""]:
            return False
        print("Digire 'n' para sim, 'n' para não ou 'c' para cancelar.")

def validar_nome(nome):
    # Validar nome não vazio.
    return nome and nome.strip() != ""
def validar_preco(preco):
    # validar preço maior que zero.
    return preco > 0
def validar_quantidade(quantidade):
    # Validar quantidade maior que zero.
    return isinstance(quantidade, int) and quantidade > 0