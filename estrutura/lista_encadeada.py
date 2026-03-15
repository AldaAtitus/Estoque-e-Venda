class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

class ListaEncadeada:
    def __init__(self):
        self.cabeca = None
        self.tamanho = 0
    
    def inserir(self, dado):
        # Insere um elemento no final da lista
        novo_no = No(dado)
        
        if self.cabeca is None:
            self.cabeca = novo_no
        else:
            atual = self.cabeca
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo_no
        
        self.tamanho += 1
        return True
    
    def buscar(self, id_busca, atributo="id"):
        # Busca um elemento por ID ou nome.
        atual = self.cabeca
        while atual:
            if atributo == "id" and hasattr(atual.dado, 'id') and atual.dado.id == id_busca:
                return atual.dado
            elif atributo == "nome" and hasattr(atual.dado, 'nome') and atual.dado.nome.lower() == id_busca.lower():
                return atual.dado
            atual = atual.proximo
        return None
    
    def remover(self, id_busca):
        # Remove um elemento por ID
        if self.cabeca is None:
            return False
        
        # Se for o primeiro elemento
        if self.cabeca.dado.id == id_busca:
            self.cabeca = self.cabeca.proximo
            self.tamanho -= 1
            return True
        
        # Procurar nos demais
        anterior = self.cabeca
        atual = self.cabeca.proximo
        
        while atual:
            if atual.dado.id == id_busca:
                anterior.proximo = atual.proximo
                self.tamanho -= 1
                return True
            anterior = atual
            atual = atual.proximo
        
        return False
    
    def listar(self):
        # Retorna todos os elementos como lista
        elementos = []
        atual = self.cabeca
        while atual:
            elementos.append(atual.dado)
            atual = atual.proximo
        return elementos
    
    def vazia(self):
        return self.cabeca is None
    
    def __len__(self):
        return self.tamanho
    
    def proximo_id(self):
        # Retorna o próximo ID que estiver disponível
        if self.vazia():
            return 1
        
        maior_id = 0
        atual = self.cabeca
        while atual:
            if atual.dado.id > maior_id:
                maior_id = atual.dado.id
            atual = atual.proximo
        
        return maior_id + 1