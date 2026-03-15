from datetime import datetime

class Produto:
    def __init__(self, id_produto, nome, quantidade, preco, data_cadastro=None):
        self.id = id_produto
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.data_cadastro = data_cadastro or datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def __str__(self):
        return f"{self.id};{self.nome};{self.quantidade};{self.preco:.2f};{self.data_cadastro}"
    
    @property
    def valor_total(self):
        return self.quantidade * self.preco
    
    @staticmethod
    def from_string(linha):
        # Cria um produto a partir de uma linha do arquivo
        try:
            partes = linha.strip().split(';')
            if len(partes) >= 4:
                produto = Produto(
                    int(partes[0]),
                    partes[1],
                    int(partes[2]),
                    float(partes[3])
                )
                if len(partes) >= 5:
                    produto.data_cadastro = partes[4]
                return produto
        except:
            return None
        return None