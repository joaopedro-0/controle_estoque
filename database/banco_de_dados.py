import sqlite3

#Conectar ao banco de dados (cria os arquivos caso não exista)
conexao = sqlite3.connect("controle_estoque.db")
cursor = conexao.cursor()


#Criação da tabela
cursor.execute('''
CREATE TABLE IF NOT EXISTS produto (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    preco_custo REAL NOT NULL,
    codigo TEXT UNIQUE NOT NULL
)
''')

conexao.commit()
conexao.close()
print(f"Banco de dados e tabelas criados com sucesso.")
