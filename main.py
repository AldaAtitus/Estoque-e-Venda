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