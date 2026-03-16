import sys
import os
import time
import traceback
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from persistencia.gerenciador_arquivos import GerenciadorArquivos
from servicos.cliente_servico import ClienteServico
from servicos.estoque_servico import EstoqueServico
from servicos.venda_servico import VendaServico
from estruturas.pilha import Pilha
from utils.validar import ler_int, ler_sim_nao
from modelos.produto import Produto
from estruturas.fila import Fila

class SistemaEstoque:
    def __init__(self):
        # Inicializa o sistema carregando os dados.
        try:
            # Carregamento automático.
            self.clientes = GerenciadorArquivos.carregar_clientes()
            self.produtos = GerenciadorArquivos.carregar_produtos()
            self.vendas = GerenciadorArquivos.carregar_vendas()
            # Pilha para desfazer operações.
            self.pilha_operacoes = Pilha()
            # Inicializar servições.
            self.cliente_servico = ClienteServico(self.clientes, self.persistir_dados)
            self.estoque_servico = EstoqueServico(self.produtos, self.persistir_dados, self.vendas, self.empilhar_operacao)
            self.venda_servico = VendaServico(self.vendas, self.cliente_servico, self.estoque_servico, self.persistir_dados, self.empilhar_operacao)

            print("\n" + "=" * 50)
            print("SISTEMA INICIADO COM SUCESSO!")
            print(f"Clientes: {len(self.clientes.listar()) if not self.clientes.vazia() else 0}")
            print(f"Produtos: {len(self.produtos.listar()) if not self.produtos.vazia() else 0}")
            print(f"Vendas: {self.vendas.tamanho()}")
            print("\n" + "=" * 50)

        except Exception as e:
            print("\n" + "=" * 50)
            print("ERRO NA INICIALIZAÇÃO!")
            print(f"Erro: {e}")
            print("\n" + "=" * 50)
            raise e
    def persistir_dados(self):
        # Salva dados automaticamente.
        try:
            GerenciadorArquivos.salvar_clientes(self.clientes)
            GerenciadorArquivos.salvar_produtos(self.produtos)
            GerenciadorArquivos.salvar_vendas(self.vendas)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            time.sleep(2)
    def empilhar_operacao(self, operacao):
        # Empilha operação para desfazer.
        self.pilha_operacoes.empilhar(operacao)
    def desfazer_operacao(self):
        # Desfaz operação.
        print("\n--- DESFAZER ÚLTIMA OPERAÇÃO ---")
        
        if self.pilha_operacoes.vazia():
            print("Nenhuma operação para desfazer.")
            return False
        try:
            operacao = self.pilha_operacoes.desempilhar()
            if operacao["tipo"] == "venda":
                # Reverter venda.
                id_produto = operacao("id_produto")
                quantidade = operacao("quantidade")
                id_cliente = operacao("id_cliente")
                valor = operacao("valor")
                print(f"\nDeseja desfazer a venda ID {operacao["id_venda"]}?")
                print(f"Cliente ID: {id_cliente}, prodito ID: {id_produto}, Quantidade: {quantidade}, Valor: R${valor:.2f}")
                confirmacao = ler_sim_nao("Confirmação? (s/n): ")

                if not confirmacao:
                    print("Operação cancelada.")
                    self.pilha_operacoes.empilhar(operacao)
                    return False
                # Repor estoque.
                self.estoque_servico.repor_estoque(id_produto, quantidade)
                # Remover venda da fila.
                self._remover_venda_da_fila(operacao["id_venda"])
                # Ajustar total gasto do cliente.
                cliente = self.cliente_servico.buscar_por_id(id_cliente)
                if cliente:
                    cliente.total_gasto -= valor
                self.persistir_dados()
                print(f"Venda {operacao["id_venda"]} desfeita com sucesso!")
                return True
            
            elif operacao["Tipo"] == "remover_produto":
                print(f"\nDeseja restaurar o produto '{operacao['nome']}' (ID: {operacao['id_produto']})?")
                print(f"Quantidade: {operacao['quantidade']}, Preco: R$ {operacao['preco']:.2f}")
                confirmacao = ler_sim_nao("Confirmação? (s/n): ")

                if not confirmacao:
                    print("Operação cancelada.")
                    self.pilha_operacoes.empilhar(operacao)
                    return False
                
                produto = Produto(operacao["id_produto"], operacao["nome"], operacao["quantidade"], operacao["preco"])
                self.estoque_servico.produtos.inserir(produto)
                self.persistir_dados()
                print(f"Produto '{operacao['nome']}' (ID: {operacao['id_produto']}) restaurado com sucesso!")
                return True
                    
            elif operacao["tipo"] == "Baixar_estoque":
                # Reverter baixa de estoque.
                print(f"\nDeseja desfazer a baixa de {operacao["quantidade_baixada"]} unidades de {operacao["nome"]}?")
                print(f"Estoque voltaria de {operacao["quantidade_anterior"] - operacao["quantidade_baixada"]} para {operacao["quantidade_anterior"]}")
                confirmacao = ler_sim_nao("Confirmação? (s/n): ")
                if confirmacao is None or not confirmacao:
                    print("Operação cancelada.")
                    self.pilha_operacoes.empilhar(operacao)
                    return False
                # Repoe o que foi baixado.
                self.estoque_servico.repor_estoque(operacao["id_produto"], operacao["quantidade_baixada"])
                self.persistir_dados()
                print("Baixa desfeita com sucesso!")
                return True
            
            elif operacao["tipo"] =="repor_estoque":
                # Reverter reposição de estoque.
                print(f"\nDeseja desfazer a reposicao de {operacao["quantidade_reposta"]} unidades de {operacao["nome"]}?")
                print(f"Estoque voltaria de {operacao["quantidade_anterior"] + operacao["quantidade_reposta"]} para {operacao["quantidade_anterior"]}")
                
                confirmacao = ler_sim_nao("Confirmação? (s/n): ")
                if confirmacao is None or not confirmacao:
                    print("Operação cancelada.")
                    self.pilha_operacoes.empilhar(operacao)
                    return False
                
                # Baixa o que foi reposto.
                self.estoque_servico.baixar_estoque(operacao["id_produto"], operacao["quantidade_reposta"])
                self.persistir_dados()
                print("Reposição desfeita com sucesso!")
                return True
            
        except Exception as e:
            print(f"Erro ao desfazer operação: {e}")
            traceback.print_exc()
            return False
        return False

    def _remover_venda_da_fila(self, id_venda):
        novas_vendas = []
        for venda in self.vendas.todos():
            if venda.id != id_venda:
                novas_vendas.append(venda)
        nova_fila = Fila()
        for v in novas vendas:
            nova_fila.enfileirar(v)
        self.vendas = nova_fila