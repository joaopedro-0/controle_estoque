import sqlite3

class Produto:
    def __init__(self, nome, quantidade, preco, preco_custo, codigo):
        if quantidade < 0 or preco < 0 or preco_custo < 0:
            raise ValueError("Quantidade e preços não podem ser negativos.")
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.preco_custo = preco_custo
        self.id = None #ID será gerado pelo banco de dados
        self.codigo = codigo
        self.criar_tabela_produto()

    def criar_tabela_produto(self):
        conexao = sqlite3.connect("controle_estoque.db")
        cursor = conexao.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS produto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            preco_custo REAL NOT NULL,
            codigo TEXT NOT NULL
            )
            ''')

        conexao.commit()
        conexao.close()

    def adicionar_estoque(self, quantidade_adicional):
        if quantidade_adicional < 0:
            raise ValueError("A quantidade adicional não pode ser negativa.")
        self.quantidade += quantidade_adicional

        conexao = sqlite3.connect("controle_estoque.db")
        cursor = conexao.cursor()
        cursor.execute('''
        UPDATE produto SET quantidade = ? WHERE codigo = ?''',(self.quantidade, self.codigo))

        conexao.commit()
        conexao.close()

    def atualizar_precos(self, novo_preco, novo_preco_custo):
        if novo_preco < 0 or novo_preco_custo < 0:
            raise ValueError("Os preços não podem ser negativos.")
        self.preco = novo_preco
        self.preco_custo = novo_preco_custo

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

    def inserir_produto(self):
        #Conectar
        conexao = sqlite3.connect("controle_estoque.db")
        cursor = conexao.cursor()
        #Inserir
        cursor.execute('''
        INSERT INTO produto (nome, quantidade, preco, preco_custo, codigo)
        VALUES  (?, ?, ?, ?, ?)
        ''', (self.nome, self.quantidade, self.preco, self.preco_custo, self.codigo))
        #Pegar o ID gerado automaticamente
        self.id= cursor.lastrowid

        conexao.commit()
        conexao.close()


    @staticmethod
    def buscar_produto(codigo):
        conexao = sqlite3.connect("controle_estoque.db")
        cursor = conexao.cursor()

        cursor.execute('''SELECT * FROM produto WHERE codigo = ?''', (codigo,))

        produto = cursor.fetchone()
        conexao.close()
        return produto

    @staticmethod
    def listar_produtos():
        conexao = sqlite3.connect("controle_estoque.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM produto")
        produtos = cursor.fetchall()

        conexao.close()
        return produtos

