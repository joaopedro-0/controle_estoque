import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.produto import Produto, criar_tabela_produto

def testar_produto():
    criar_tabela_produto()
    #Criar uma instância da classe Produto
    produto = Produto(nome="Air Jordan", quantidade=10, preco=1299.00, preco_custo=699.99, codigo="548930324")

    #Inserir o produto no banco de dados
    produto.inserir_produto()

    #Testar a representação do produto
    print(produto)

    #Testar adicionar estoque
    produto.adicionar_estoque(4)
    print(f"Após adicionar 4 unidades: {produto.quantidade} unidades")

    #Testar atualizar preço
    produto.atualizar_precos(0, 0)
    print(f"Novo preço de venda: {produto.preco}, novo preço de custo: {produto.preco_custo}")

    #Testar cálculo de lucro e markup
    print(f"Markup: {produto.calcular_markup():.2f}")
    print(f"Lucro: {produto.calcular_lucro():.2f}")

    #Testar exceção ao tentar adicionar quantidade negativa
    try:
        produto.adicionar_estoque(-3)
    except ValueError as e:
        print(e)

    #Buscar o produto no banco de dados e imprimir os dados
    codigo_busca = "123456890"
    produto_buscado = produto.buscar_produto(codigo_busca)
    if produto_buscado:
        print("Produto encontrado no banco de dados", produto_buscado)
    else:
        print("Produto não encontrado")

if __name__ == "__main__":
    testar_produto()
