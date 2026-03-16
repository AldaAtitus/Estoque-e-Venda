from datetime import datetime

class Cliente:
    def __init__(self, id_cliente, nome, data_cadastro=None):
        self.id = id_cliente
        self.nome = nome
        self.total_gasto = 0
        self.data_cadastro = data_cadastro or datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def __str__(self):
        return f"{self.id};{self.nome};{self.total_gasto:.2f};{self.data_cadastro}"
    
    @staticmethod
    def from_string(linha):
        # Cria um cliente a partir de uma linha do arquivo
        try:
            partes = linha.strip().split(';')
            if len(partes) >= 3:
                cliente = Cliente(int(partes[0]), partes[1])
                cliente.total_gasto = float(partes[2])
                if len(partes) >= 4:
                    cliente.data_cadastro = partes[3]
                return cliente
        except:
            return None
        return None