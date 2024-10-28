class Produto:
    def __init__(self, nome, quantidade, preco, preco_custo, id, codigo):
        if quantidade < 0 or preco < 0 or preco_custo < 0:
            raise ValueError("Quantidade e preços não podem ser negativos.")
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.preco_custo = preco_custo
        self.id = id
        self.codigo = codigo

    def adicionar_estoque(self, quantidade_adicional):
        if quantidade_adicional < 0:
            raise ValueError("A quantidade adicional não pode ser negativa.")
        self.quantidade += quantidade_adicional

    def atualizar_precos(self, novo_preco, novo_preco_custo):
        if novo_preco < 0 or novo_preco_custo < 0:
            raise ValueError("Os preços não podem ser negativos.")
        self.preco = novo_preco
        self.preco_custo = novo_preco_custo
    def atualizar_quantidade(self, nova_quantidade):
        self.quantidade = nova_quantidade

    def calcular_markup(self):
        return (self.preco - self.preco_custo) / self.preco_custo if self.preco_custo else 0

    def calcular_lucro(self):
        return self.preco - self.preco_custo

    def __str__(self):
        return (f"Produto: {self.nome}, "
                f"Quantidade: {self.quantidade}, "
                f"Preço de venda: {self.preco:.2f}, "
                f"Preço de custo: {self.preco_custo:.2f}, "
                f"ID: {self.id}, "
                f"Código de barras: {self.codigo}, "
                f"Markup: {self.calcular_markup():.2f}, "
                f"Lucro: {self.calcular_lucro():.2f} ")

