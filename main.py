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
from utils.validar import let_int, ler_sim_nao

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
        print("\n--- DESFAZER ÚLTIMA OPERAÇÃO ---"))