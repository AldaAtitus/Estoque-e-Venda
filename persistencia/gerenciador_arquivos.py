import os

class GerenciadorArquivos:
    # Gerencia persistência em arquivos .txt
    
    @staticmethod
    def garantir_diretorio():
        # Garante que o diretório "dados" exista
        os.makedirs("dados", exist_ok=True)
    
    @staticmethod
    def carregar_clientes(caminho="dados/clientes.txt"):
        # Carrega os clientes do arquivo .txt
        from modelos.cliente import Cliente
        from estruturas.lista_encadeada import ListaEncadeada
        
        clientes = ListaEncadeada()
        GerenciadorArquivos.garantir_diretorio()
        
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if linha and not linha.startswith("#"):
                        cliente = Cliente.from_string(linha)
                        if cliente:
                            clientes.inserir(cliente)
        except FileNotFoundError:
            GerenciadorArquivos.salvar_clientes(clientes, caminho)
        except Exception as e:
            print(f"Erro ao carregar clientes: {e}")
        
        return clientes
    
    @staticmethod
    def salvar_clientes(clientes, caminho="dados/clientes.txt"):
        # Salva os clientes no arquivo .txt
        GerenciadorArquivos.garantir_diretorio()
        
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write("# ID|Nome|CPF|Telefone|Email\n")
                for cliente in clientes.listar():
                    arquivo.write(f"{cliente}\n")
        except Exception as e:
            print(f"Erro ao salvar clientes: {e}")
    
    @staticmethod
    def carregar_produtos(caminho="dados/produtos.txt"):
        # Carrega os produtos do arquivo .txt
        from modelos.produto import Produto
        from estruturas.lista_encadeada import ListaEncadeada
        
        produtos = ListaEncadeada()
        GerenciadorArquivos.garantir_diretorio()
        
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if linha and not linha.startswith("#"):
                        produto = Produto.from_string(linha)
                        if produto:
                            produtos.inserir(produto)
        except FileNotFoundError:
            GerenciadorArquivos.salvar_produtos(produtos, caminho)
        except Exception as e:
            print(f"Erro ao carregar produtos: {e}")
        
        return produtos
    
    @staticmethod
    def salvar_produtos(produtos, caminho="dados/produtos.txt"):
        # Salva os produtos no arquivo .txt
        GerenciadorArquivos.garantir_diretorio()
        
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write("# ID;NOME;QUANTIDADE;PRECO;DATA_CADASTRO\n")
                for produto in produtos.listar():
                    arquivo.write(f"{produto}\n")
        except Exception as e:
            print(f"Erro ao salvar produtos: {e}")
    
    @staticmethod
    def carregar_vendas(caminho="dados/vendas.txt"):
        # Carrega as vendas do arquivo .txt
        from modelos.venda import Venda
        from estruturas.fila import Fila
        
        vendas = Fila()
        GerenciadorArquivos.garantir_diretorio()
        
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if linha and not linha.startswith("#"):
                        venda = Venda.from_string(linha)
                        if venda:
                            vendas.enfileirar(venda)
        except FileNotFoundError:
            GerenciadorArquivos.salvar_vendas(vendas, caminho)
        except Exception as e:
            print(f"Erro ao carregar vendas: {e}")
        
        return vendas
    
    @staticmethod
    def salvar_vendas(vendas, caminho="dados/vendas.txt"):
        # Salva as vendas no .txt
        GerenciadorArquivos.garantir_diretorio()
        
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write("# ID;ID_CLIENTE;ID_PRODUTO;QUANTIDADE;VALOR_TOTAL;DATA_VENDA\n")
                for venda in vendas.listar():
                    arquivo.write(f"{venda}\n")
        except Exception as e:
            print(f"Erro ao salvar vendas: {e}")