from models.produto import Produto

def testar_produto():
    #Criar uma instância da classe Produto
    produto = Produto(nome="Adidas Samba", quantidade=10, preco=699.99, preco_custo=349.99, id=1, codigo="1234567890")

    #Testar a representação do produto
    print(produto)

    #Testar adicionar estoque
    produto.adicionar_estoque(4)
    print(f"Após adicionar 4 unidades: {produto.quantidade} unidades")

    #Testar atualizar preço
    produto.atualizar_precos(749.99, 374.99)
    print(f"Novo preço de venda: {produto.preco}, novo preço de custo: {produto.preco_custo}")

    #Testar cálculo de lucro e markup
    print(f"Markup: {produto.calcular_markup():.2f}")
    print(f"Lucro: {produto.calcular_lucro():.2f}")

    #Testar exceção ao tentar adicionar quantidade negativa
    try:
        produto.adicionar_estoque(-3)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    testar_produto()
