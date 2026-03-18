from utils.validar import ler_string, ler_int, ler_sim_nao
import time

class ClienteServico:
    def __init__(self, clientes, persistir_callback, vendas=None, empilhar_operacao=None):
        self.clientes = clientes
        self.persistir = persistir_callback
        self.vendas = vendas
        self.empilhar_operacao = empilhar_operacao
        
    def cadastrar(self):
        #Cadastra cliente com ID escolhido pelo usuário
        print("\n--- CADASTRAR CLIENTE ---")
        print("(Digite 'C' a qualquer momento para cancelar)")
        
        #Escolhe ID
        while True:
            id_cliente = ler_int("ID do cliente: ", permitir_cancelar=True)
            if id_cliente is None:
                return False
            
            #Verifica se já existe ID
            if self.clientes.buscar(id_cliente, "id") is not None:
                print(f"ID {id_cliente} já existe! Escolha outro ID.")
                continue
            
            if id_cliente <= 0:
                print("ID deve ser maior que zero.")
                continue
            
            break
        
        nome = ler_string("Nome do cliente: ")
        if nome is None:
            return False
        
        print(f"\nCliente: ID {id_cliente} - {nome}")
        confirmacao = ler_sim_nao("Confirmar cadastro? (s/n): ")
        if confirmacao is None or not confirmacao: # Cancela se usuário digitou 'c' ou 'n'
            print("Cadastro cancelado.")
            return False
        
        from modelos.cliente import Cliente
        cliente = Cliente(id_cliente, nome)
        
        self.clientes.inserir(cliente)
        self.persistir()
        print(f"Cliente {nome} cadastrado com ID {id_cliente}!")
        return cliente

    def listar(self):
    # Lista todos os clientes com data de cadastro
        print("\n--- LISTA DE CLIENTES ---")
        if self.clientes.vazia():
            print("Nenhum cliente cadastrado.")
            return
        
        print("ID  | NOME                 | DATA CADASTRO")
        print("-" * 50)
        for cliente in self.clientes.listar():
            data = cliente.data_cadastro if hasattr(cliente, 'data_cadastro') else "sem data"
            print(f"{cliente.id:<4} | {cliente.nome:<20} | {data}")
            
    def buscar_por_id(self, id_cliente):
        # Busca cliente pelo ID
        return self.clientes.buscar(id_cliente, "id")

    def atualizar_total_gasto(self, id_cliente, valor):
        # Atualiza o total gasto do cliente
        cliente = self.buscar_por_id(id_cliente)
        if cliente:
            cliente.total_gasto += valor
            self.persistir()
            return True
        return False
    
    def exibir_rank_gastos(self):
        # Exibe clientes e valores totais gastos
        print("\n--- CLIENTES E VALORES GASTOS ---")
        if self.clientes.vazia():
            print("Nenhum cliente cadastrado.")
            return
        
        clientes_lista = self.clientes.listar()
        clientes_ordenados = sorted(clientes_lista, key=lambda c: c.total_gasto, reverse=True)
        print("ID | Nome                 | Total Gasto")
        print("-"*50)
        for cliente in clientes_ordenados:
            print(f"{cliente.id:<4} | {cliente.nome:<20} | R$ {cliente.total_gasto:.2f}")
    
    def remover_cliente(self):
        # Remove cliente do sistema
        print("\n--- REMOVER CLIENTE ---")
        print("(Digite 'C' para cancelar)")
        
        if self.clientes.vazia():
            print("Nenhum cliente cadastrado para remover.")
            return False
        
        self.listar()
        id_cliente = ler_int("ID do cliente a remover: ", permitir_cancelar=True)
        if id_cliente is None:
            return False
        
        cliente = self.buscar_por_id(id_cliente)
        if cliente is None:
            print(f"Cliente com ID {id_cliente} não encontrado.")
            return False

        print(f"\nCliente selecionado:")
        print(f"   ID: {cliente.id}")
        print(f"   Nome: {cliente.nome}")
        print(f"   Total Gasto: R$ {cliente.total_gasto:.2f}")
        
        #Verifica se cliente tem vendas
        if self.vendas:
            vendas_cliente = []
            for venda in self.vendas.todos():
                if venda.id_cliente == id_cliente:
                    vendas_cliente.append(venda)
            
            if vendas_cliente:
                print(f"\nATENÇÃO: Este cliente possui {len(vendas_cliente)} venda(s) no histórico!")
                confirmar = ler_sim_nao("Remover mesmo assim? (O historico de vendas será mantido) (s/n): ")
                
                if confirmar is None or not confirmar:
                    print("Remoção cancelada.")
                    return False
                
        confirmacao = ler_sim_nao("\nTem certeza que deseja REMOVER este cliente? (s/n): ")
        if confirmacao is None or not confirmacao:
            print("Remoção cancelada.")
            return False
        
        # Registra operação para desfazer
        if self.empilhar_operacao:
            operacao = {
                'tipo': 'remover_cliente',
                'id_cliente': cliente.id,
                'nome': cliente.nome,
                'total_gasto': cliente.total_gasto,
                'timestamp': time.time()
            }
            self.empilhar_operacao(operacao)
        
        if self.clientes.remover(id_cliente):
            self.persistir()
            print(f"\nCliente '{cliente.nome}' (ID: {id_cliente}) removido com sucesso!")
            print("   Para desfazer, use a opcao 11 - Desfazer ultima operacao")
            return True
        else:
            print(f"\nErro ao remover cliente. Tente novamente.")
            return False
        
    def pesquisar_cliente(self):
    # Pesquisa clientes por ID ou nome
        print("\n--- PESQUISAR CLIENTE ---")
        print("(Digite 'C' para cancelar e voltar ao menu)")
        
        while True:
            print("\n1 - Pesquisar por ID")
            print("2 - Pesquisar por nome")
            opcao = ler_int("Escolha: ", permitir_cancelar=True) 
            if opcao == 1:
                self._pesquisar_cliente_por_id()
                break
            elif opcao == 2:
                self._pesquisar_cliente_por_nome()
                break
            elif opcao is None:
                print("Pesquisa cancelada.")
                return
            else:
                print("Opção inválida! Digite 1, 2 ou 'C' para cancelar.")
        
    def _pesquisar_cliente_por_id(self):
        while True:
            id_cliente = ler_int("Digite o ID do cliente: ", permitir_cancelar=True)
            cliente = self.buscar_por_id(id_cliente)
            if cliente:
                self._exibir_cliente(cliente)
                return
            elif id_cliente is None:
                print("Pesquisa cancelada.")
                return
            else:
                print(f"Cliente com ID {id_cliente} não encontrado!")
                tentar = ler_sim_nao("Tentar novamente? (s/n): ")
                if tentar is None or not tentar:
                    print("Pesquisa cancelada.")
                    return
        
    def _pesquisar_cliente_por_nome(self):
        while True:
            nome = ler_string("Digite o nome do cliente: ", permitir_cancelar=True)
            if nome is None:
                print("Pesquisa cancelada.")
                return
            
            # Busca por nome
            cliente_encontrado = None
            for cliente in self.clientes.listar():
                if cliente.nome.lower() == nome.lower():
                    cliente_encontrado = cliente
                    break
            
            if cliente_encontrado:
                self._exibir_cliente(cliente_encontrado)
                return
            
            else:
                print(f"Cliente '{nome}' não encontrado!")
                tentar = ler_sim_nao("Tentar novamente? (s/n): ")
                if tentar is None or not tentar:
                    print("Pesquisa cancelada.")
                    return
                
    def _exibir_cliente(self, cliente):
        # Exibe detalhes de um cliente
        print("\nDETALHES DO CLIENTE:")
        print(f"ID: {cliente.id}")
        print(f"Nome: {cliente.nome}")
        print(f"Total gasto: R$ {cliente.total_gasto:.2f}")
        if hasattr(cliente, 'data_cadastro'):
            print(f"Data cadastro: {cliente.data_cadastro}")