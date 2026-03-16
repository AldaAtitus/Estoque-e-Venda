from datetime import datetime

class Venda:
    def __init__(self, id_venda, id_cliente, id_produto, quantidade, valor_total, data_venda=None):
        self.id = id_venda
        self.id_cliente = id_cliente
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.valor_total = valor_total
        self.data_venda = data_venda or datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def __str__(self):
        return f"{self.id};{self.id_cliente};{self.id_produto};{self.quantidade};{self.valor_total:.2f};{self.data_venda}"
    
    @staticmethod
    def from_string(linha):
        # Cria uma venda a partir de uma linha do arquivo
        try:
            partes = linha.strip().split(';')
            if len(partes) >= 5:
                venda = Venda(
                    int(partes[0]),
                    int(partes[1]),
                    int(partes[2]),
                    int(partes[3]),
                    float(partes[4])
                )
                if len(partes) >= 6:
                    venda.data_venda = partes[5]
                return venda
        except:
            return None
        return None