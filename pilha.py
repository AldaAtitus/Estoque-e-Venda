class Pilha:
    def __init__(self):
        self.items = []
    
    def empilhar(self, item):
        # Adiciona item ao topo da pilha
        self.items.append(item)
    
    def desempilhar(self):
        # Remove e retorna o item do topo
        if not self.vazia():
            return self.items.pop()
        return None
    
    def topo(self):
        # Retorna o item do topo sem remover.
        if not self.vazia():
            return self.items[-1]
        return None
    
    def vazia(self):
        return len(self.items) == 0
    
    def tamanho(self):
        return len(self.items)
    
    def limpar(self):
        # Limpa tudo
        self.items = []