def ler_int(mensagem, permitir_cancelar=True):
    # Lê um número inteiro com tratamento de erros
    while True:
        try:
            valor = input(mensagem).strip()
            # Verificar cancelamento ("c ou C")
            if permitir_cancelar and valor.lower() == "c":
                print("Operação cancelada. Voltando ao menu principal.")
                return None
            return int(valor)
        except ValueError:
            print("Entrada inválida. Por favor, digite um número válido ou 'C' para cancelar.")
