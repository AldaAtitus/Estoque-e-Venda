from utils.validar import ler_string, ler_int, ler_float, ler_sim_nao, validar_preco, validar_quantidade
from modelos.produto import Produto
import time

class EstoqueServico:
    def __init__(self, produtos, persistir_callback, vendas=None, empilhar_operacao=None):
        self.produtos = produtos
        self.persistir = persistir_callback
        self.vendas = vendas
        self.empilhar_operacao = empilhar_operacao
    
    def cadastrar(self):
        # Cadastra produto com ID escolhido pelo usuário
        print("\n--- CADASTRAR PRODUTO ---")
        print("(Digite 'C' a qualquer momento para cancelar)")

        while True:
            id_produto = ler_int("ID do produto: ", permitir_cancelar=True)
            if id_produto is None:
                return False
            
            # Verifica se ID já existe
            if self.produtos.buscar(id_produto, "id") is not None:
                print(f"ID {id_produto} já existe! Escolha outro ID.")
                continue
            
            if id_produto <= 0:
                print("ID deve ser maior que zero!")
                continue
            break
        
        nome = ler_string("Nome do produto: ")
        if nome is None:
            return False
        
        quantidade = ler_int("Quantidade em estoque: ")
        if quantidade is None:
            return False
        while not validar_quantidade(quantidade):
            print("Quantidade deve ser maior que zero!")
            quantidade = ler_int("Quantidade em estoque: ")
            if quantidade is None:
                return False
        
        preco = ler_float("Preço unitário: R$ ")
        if preco is None:
            return False
        while not validar_preco(preco):
            print("Preço deve ser maior que zero!")
            preco = ler_float("Preço unitário: R$ ")
            if preco is None:
                return False
        
        print(f"\nProduto: ID {id_produto} - {nome}")
        print(f"Quantidade: {quantidade}")
        print(f"Preço: R$ {preco:.2f}")
        print(f"Valor total: R$ {quantidade * preco:.2f}")
        
        #Confirma
        confirmacao = ler_sim_nao("Confirma cadastro? (s/n): ")
        if confirmacao is None or not confirmacao:
            print("Cadastro cancelado.")
            return False
        
        produto = Produto(id_produto, nome, quantidade, preco)
        self.produtos.inserir(produto)
        self.persistir()
        print(f"Produto '{nome}' cadastrado com ID {id_produto}!")
        return produto
    
    def listar(self):
        print("\n--- LISTA DE PRODUTOS ---")
        
        if self.produtos.vazia():
            print("Nenhum produto cadastrado.")
            return
        
        print("ID  | NOME                 | QTD  | PRECO    | TOTAL")
        print("-" * 60)
        for produto in self.produtos.listar():
            print(f"{produto.id:<4} | {produto.nome:<20} | {produto.quantidade:<4} | R$ {produto.preco:<7.2f} | R$ {produto.valor_total:.2f}")
            
    def pesquisar(self):
        # Pesquisa produto por nome ou ID
        print("\n--- PESQUISAR PRODUTO ---")
        print("(Digite 'C' para cancelar e voltar ao menu)")
        
        while True:
            print("\n1 - Pesquisar por ID")
            print("2 - Pesquisar por nome")
            
            opcao = ler_int("Escolha: ", permitir_cancelar=True)
            if opcao == 1:
                self._pesquisar_produto_por_id()
                break
            elif opcao == 2:
                self._pesquisar_produto_por_nome()
                break
            elif opcao is None:
                print("Pesquisa cancelada.")
                return
            else:
                print("Opção inválida! Digite 1, 2 ou 'C' para cancelar.")
                
    def _pesquisar_produto_por_id(self):
        while True:
            id_produto = ler_int("Digite o ID do produto: ", permitir_cancelar=True)
            if id_produto is None:
                print("Pesquisa cancelada.")
                return
            
            produto = self.produtos.buscar(id_produto, "id")
            if produto:
                self._exibir_produto(produto)
                return
            else:
                print(f"Produto com ID {id_produto} não encontrado!")
                tentar = ler_sim_nao("Tentar novamente? (s/n): ")
                if tentar is None or not tentar:
                    print("Pesquisa cancelada.")
                    return
                
    def _pesquisar_produto_por_nome(self):
        while True:
            nome = ler_string("Digite o nome do produto: ", permitir_cancelar=True)
            if nome is None:
                print("Pesquisa cancelada.")
                return
            
            produto = self.produtos.buscar(nome, "nome")
            if produto:
                self._exibir_produto(produto)
                return
            else:
                print(f"Produto '{nome}' não encontrado!")
                tentar = ler_sim_nao("Tentar novamente? (s/n): ")
                if tentar is None or not tentar:
                    print("Pesquisa cancelada.")
                    return
                
    def _exibir_produto(self, produto):
        print("\nDETALHES DO PRODUTO:")
        print(f"ID: {produto.id}")
        print(f"Nome: {produto.nome}")
        print(f"Quantidade: {produto.quantidade}")
        print(f"Preço: R$ {produto.preco:.2f}")
        print(f"Valor total em estoque: R$ {produto.valor_total:.2f}")
        
    def buscar_por_id(self, id_produto):
        return self.produtos.buscar(id_produto, "id")
    
    def verificar_disponibilidade(self, id_produto, quantidade):
        produto = self.buscar_por_id(id_produto)
        if produto and produto.quantidade >= quantidade:
            return True
        return False
    
    def baixar_estoque(self, id_produto, quantidade):
        produto = self.buscar_por_id(id_produto)
        if produto and produto.quantidade >= quantidade:
            produto.quantidade -= quantidade
            self.persistir()
            return True
        return False
    
    def repor_estoque(self, id_produto, quantidade):
        produto = self.buscar_por_id(id_produto)
        if produto:
            produto.quantidade += quantidade
            self.persistir()
            return True
        return False
    
    def remover_produto(self):
        print("\n--- REMOVER PRODUTO ---")
        print("(Digite 'C' para cancelar)")
        
        if self.produtos.vazia():
            print("Nenhum produto cadastrado para remover.")
            return False
        
        self.listar()
        id_produto = ler_int("\nID do produto a remover: ", permitir_cancelar=True)
        if id_produto is None:
            return False
        
        produto = self.buscar_por_id(id_produto)
        if produto is None:
            print(f"Produto com ID {id_produto} não encontrado!")
            return False
        
        print(f"\nProduto selecionado:")
        print(f"   ID: {produto.id}")
        print(f"   Nome: {produto.nome}")
        print(f"   Quantidade: {produto.quantidade}")
        print(f"   Preço: R$ {produto.preco:.2f}")
        print(f"   Valor total: R$ {produto.valor_total:.2f}")
        
        # Verifica se há estoque
        if produto.quantidade > 0:
            print(f"\nATENÇÃO: Este produto ainda tem {produto.quantidade} unidades em estoque!")
            confirmar = ler_sim_nao("Remover mesmo assim? (s/n): ")
            
            if confirmar is None or not confirmar:
                print("Remoção cancelada.")
                return False
            
        # Verifica vendas associadas
        if self.vendas:
            vendas_associadas = False
            for venda in self.vendas.todos():
                if venda.id_produto == id_produto:
                    vendas_associadas = True
                    break
            
            if vendas_associadas:
                print(f"\nATENÇÃO: Este produto possui vendas registradas no histórico!")
                confirmar = ler_sim_nao("Remover mesmo assim? (O historico sera mantido) (s/n): ")
                
                if confirmar is None or not confirmar:
                    print("Remoção cancelada.")
                    return False
                
        # Confirma remoção
        confirmacao = ler_sim_nao("\nTem certeza que deseja REMOVER este produto? (s/n): ")
        if confirmacao is None or not confirmacao:
            print("Remoção cancelada.")
            return False
        
        # Registra operação para desfazer
        if self.empilhar_operacao:
            operacao = {
                'tipo': 'remover_produto',
                'id_produto': produto.id,
                'nome': produto.nome,
                'quantidade': produto.quantidade,
                'preco': produto.preco,
                'timestamp': time.time()
            }
            self.empilhar_operacao(operacao)
            
        if self.produtos.remover(id_produto):
            self.persistir()
            print(f"\nProduto '{produto.nome}' (ID: {id_produto}) removido com sucesso!")
            print("   Para desfazer, use a opção 11 - Desfazer última operação")
            return True
        else:
            print(f"\nErro ao remover produto. Tente novamente.")
            return False