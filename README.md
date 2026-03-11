# Mini Sistema de Estoque e Vendas

## Disciplina
Ciência da Computação - Organização e Abstração na Programação

## Título do Trabalho
Sistema de Estoque e Vendas com Persistência em Arquivos .txt

## Integrantes
- Aldacir Stanguerlin Junior | 1137226
- Henrique Machado de Lima |1136129
- Adriano Cezar Tessaro Junior | 1138080

## Descrição do Sistema
Sistema desenvolvido em Python para gerenciamento de estoque e vendas, executado no terminal. 
Permite cadastro de clientes e produtos, realização de vendas, consultas, remoção de itens e 
desfazimento da última operação, com persistência automática em arquivos .txt.

### Funcionalidades principais:
- Cadastrar, listar, pesquisar e remover clientes
- Cadastrar, listar, pesquisar e remover produtos
- Realizar vendas com validação de estoque
- Visualizar fila de vendas
- Desfazer última operação (venda ou remoção)
- Exibir valor total do estoque e de vendas
- Exibir ranking de clientes por valor gasto

## Estruturas de Dados Utilizadas

### 1. Lista Encadeada
Utilizada para armazenar **clientes** e **produtos**. Implementada manualmente com nós 
encadeados, permitindo inserção no final, busca por ID ou nome, e remoção por ID.

### 2. Fila (FIFO)
Utilizada para armazenar as **vendas** na ordem em que ocorrem (First In, First Out). 
Permite visualizar o histórico sequencial de vendas.

### 3. Pilha (LIFO)
Utilizada para implementar a funcionalidade de **desfazer última operação** (Last In, 
First Out). Cada venda ou remoção é empilhada e pode ser desfeita posteriormente.

## Persistência Automática em Arquivos
O sistema utiliza arquivos .txt como banco de dados, com carregamento e salvamento automáticos.

### Arquivos gerados:
- **clientes.txt**: ID;NOME;TOTAL_GASTO;DATA_CADASTRO
- **produtos.txt**: ID;NOME;QUANTIDADE;PRECO;DATA_CADASTRO
- **vendas.txt**: ID;ID_CLIENTE;ID_PRODUTO;QUANTIDADE;VALOR_TOTAL;DATA_VENDA

### Características:
- Carregamento automático ao iniciar o sistema
- Salvamento automático a cada alteração
- Criação automática dos arquivos se não existirem
- Tratamento de erros na leitura/escrita

## Instruções de Execução

### Pré-requisitos
- Python 3.6 ou superior

### Passos para executar

1. **Clone o repositório:**
```bash
git clone https://github.com/AldaAtitus/Estoque-e-Venda.git
cd projeto_estoque
python main.py
