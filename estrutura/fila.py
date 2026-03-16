class Fila:
    def __init__(self):
        self.items = []
    
    def enfileirar(self, item):
        # Adiciona item ao final da fila.
        self.items.append(item)
    
    def desenfileirar(self):
        # Remove e retorna o primeiro item da fila
        if not self.vazia():
            return self.items.pop(0)
        return None
    
    def primeiro(self):
        # Retorna o primeiro item sem remover
        if not self.vazia():
            return self.items[0]
        return None
    
    def vazia(self):
        return len(self.items) == 0
    
    def todos(self):
        # Retorna todos os itens da fila
        return self.items.copy()
    
    def tamanho(self):
        return len(self.items)
    
    def limpar(self):
        # Limpa a fila inteiramente
        self.items = []