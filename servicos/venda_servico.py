from modelos.venda import Venda
from utils.validar import ler_int, ler_sim_nao
import time
import traceback

class VendaServico:
    def __init__(self, vendas, clientes_servico, estoque_servico, persistir_callback, empilhar_operacao):
        self.vendas = vendas
        self.clientes_servico = clientes_servico
        self.estoque_servico = estoque_servico
        self.persistir = persistir_callback
        self.empilhar_operacao = empilhar_operacao

    def realizar(self):
        # Realiza uma nova venda
        try:
            print("\n--- REALIZAR VENDA ---")
            print("(Digite 'C' para cancelar a qualquer momento)")

            if self.clientes_servico.clientes.vazia():
                print("Não é possível vender: nenhum cliente cadastrado!")
                return False

            if self.estoque_servico.produtos.vazia():
                print("Não é possível vender: nenhum produto cadastrado!")
                return False

            # Selecionar cliente
            self.clientes_servico.listar()
            id_cliente = ler_int("ID do cliente: ", permitir_cancelar=True)
            if id_cliente is None:  # Cancelou
                return False
            
            cliente = self.clientes_servico.buscar_por_id(id_cliente)
            if not cliente:
                print(f"Cliente com ID {id_cliente} não encontrado!")
                return False

            # Selecionar produto
            self.estoque_servico.listar()
            id_produto = ler_int("ID do produto: ", permitir_cancelar=True)
            if id_produto is None:  # Cancelou
                return False
            
            produto = self.estoque_servico.buscar_por_id(id_produto)
            if not produto:
                print(f"Produto com ID {id_produto} não encontrado!")
                return False

            # Quantidade
            print(f"Disponível em estoque: {produto.quantidade}")
            quantidade = ler_int("Quantidade: ", permitir_cancelar=True)
            if quantidade is None:  # Cancelou
                return False
            
            if quantidade <= 0:
                print("Quantidade deve ser maior que zero!")
                return False

            # Verificar estoque
            if not self.estoque_servico.verificar_disponibilidade(id_produto, quantidade):
                print(f"Estoque insuficiente! Disponível: {produto.quantidade}")
                return False

            # Calcular valor total
            valor_total = quantidade * produto.preco
            print("\nRESUMO DA VENDA:")
            print(f"Cliente: {cliente.nome} (ID: {cliente.id})")
            print(f"Produto: {produto.nome} (ID: {produto.id})")
            print(f"Quantidade: {quantidade}")
            print(f"Preço unitário: R$ {produto.preco:.2f}")
            print(f"Valor total: R$ {valor_total:.2f}")
            
            # Confirmar venda
            confirmacao = ler_sim_nao("\nConfirmar venda? (s/n): ")
            if confirmacao is None or not confirmacao:
                print("Venda cancelada.")
                return False

            # Processa venda
            id_venda = self.vendas.tamanho() + 1
            venda = Venda(id_venda, id_cliente, id_produto, quantidade, valor_total)
            self.vendas.enfileirar(venda)
            self.estoque_servico.baixar_estoque(id_produto, quantidade)
            self.clientes_servico.atualizar_total_gasto(id_cliente, valor_total)
            operacao = {
                'tipo': 'venda',
                'id_venda': id_venda,
                'id_cliente': id_cliente,
                'id_produto': id_produto,
                'quantidade': quantidade,
                'valor': valor_total,
                'timestamp': time.time()
            }
            self.empilhar_operacao(operacao)
            self.persistir()
            print(f"\nVenda realizada com sucesso!")
            print(f"ID da venda: {id_venda}")
            print(f"Valor total: R$ {valor_total:.2f}")
            return True

        except Exception as e:
            print(f"\nERRO NA VENDA: {e}")
            traceback.print_exc()
            print("\nO erro será tratado pelo sistema principal...")
            time.sleep(3)
            raise e
    
    def visualizar_fila(self):
    # Visualiza a fila de vendas
        try:
            print("\n--- FILA DE VENDAS ---")
            if self.vendas.vazia():
                print("Nenhuma venda registrada.")
                return

            print("Ordem | ID Venda | Cliente | Produto | QTD | Valor     | Data/Hora")
            print("-" * 80)
            for i, venda in enumerate(self.vendas.todos(), 1):
                cliente = self.clientes_servico.buscar_por_id(venda.id_cliente)
                produto = self.estoque_servico.buscar_por_id(venda.id_produto)
                nome_cliente = cliente.nome[:10] if cliente else "Desconhecido"
                nome_produto = produto.nome[:10] if produto else "Desconhecido"
                
                # Mostrar data (ou "sem data" se não tiver)
                data = venda.data_venda if hasattr(venda, 'data_venda') else "sem data"
                print(f"{i:<6} | {venda.id:<7} | {nome_cliente:<10} | {nome_produto:<10} | {venda.quantidade:<3} | R$ {venda.valor_total:<7.2f} | {data}")

        except Exception as e:
            print(f"Erro ao visualizar fila: {e}")
            time.sleep(2)
            
    def valor_total_vendas(self):
        # Calcula o valor total de todas as vendas
        try:
            total = 0
            for venda in self.vendas.todos():
                total += venda.valor_total
            return total
        except Exception as e:
            print(f"Erro ao calcular total de vendas: {e}")
            return 0
        
    def quantidade_total_vendas(self):
        # Calcula a quantidade total de vendas realizadas
        try:
            quantidade = 0
            for venda in self.vendas.todos():
                quantidade += venda.quantidade
            return quantidade
        except Exception as e:
            print(f"Erro ao calcular quantidade total de vendas: {e}")
            return 0