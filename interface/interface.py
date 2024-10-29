import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
import sqlite3
import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from models.produto import Produto

def salvar_produto():
    #Captura os dados inseridos pelo usuário
    nome = nome_entrada.get()
    quantidade = quantidade_entrada.get()
    preco = preco_entrada.get().replace(',', '.')
    preco_custo = preco_custo_entrada.get().replace(',', '.')
    codigo = codigo_entrada.get()

    #Validação de números
    try:
        quantidade = int(quantidade)
        preco = float(preco.replace(',', '.'))
        preco_custo = float(preco_custo.replace(',', '.'))
    except ValueError:
        messagebox.showerror("Erro", "Certifique-se de que seja valores númericos.")
        return

    #Criação do produto e de salvar no banco de dados
    try:
        produto = Produto(nome=nome, quantidade=quantidade, preco=preco, preco_custo=preco_custo, codigo=codigo)
        produto.inserir_produto()
        messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar produto: {e}")

    #Limpar os campos após salvar
    nome_entrada.delete(0, tk.END)
    quantidade_entrada.delete(0, tk.END)
    preco_entrada.delete(0, tk.END)
    preco_custo_entrada.delete(0, tk.END)
    codigo_entrada.delete(0, tk.END)

#Configuração da janela principal
root = tk.Tk()
root.title("EstokPRO")
root.geometry("400x300")

#Elementos da interface
tk.Label(root, text="Nome do produto:").pack()
nome_entrada = tk.Entry(root)
nome_entrada.pack()

tk.Label(root, text="Quantidade:").pack()
quantidade_entrada = tk.Entry(root)
quantidade_entrada.pack()

tk.Label(root, text="Preço de venda:").pack()
preco_entrada = tk.Entry(root)
preco_entrada.pack()

tk.Label(root, text="Preço de custo:").pack()
preco_custo_entrada = tk.Entry(root)
preco_custo_entrada.pack()

tk.Label(root, text="Código de barras:").pack()
codigo_entrada = tk.Entry(root)
codigo_entrada.pack()

#Botão de salvar
tk.Button(root, text="Salvar produto", command=salvar_produto).pack(pady=10)

def mostrar_estoque():
    conexao = sqlite3.connect("controle_estoque.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, quantidade, preco, preco_custo, codigo FROM produto")
    produtos = cursor.fetchall()
    conexao.close()

    #Janela lista de estoque
    estoque_janela = Toplevel(root)
    estoque_janela.title("Lista de estoque")
    estoque_janela.geometry("600x400")

    #Nome de cada coluna
    colunas = ("nome", "quantidade", "preco", "preco_custo", "codigo", "markup", "lucro")
    tabela_estoque = ttk.Treeview(estoque_janela, columns=colunas, show="headings")

    #Indicando a escrita de cada coluna
    tabela_estoque.heading("nome", text="Nome")
    tabela_estoque.heading("quantidade", text="Quantidade")
    tabela_estoque.heading("preco", text="Preço")
    tabela_estoque.heading("preco_custo", text="Preço custo")
    tabela_estoque.heading("codigo", text="Código")
    tabela_estoque.heading("markup", text="MarkUp")
    tabela_estoque.heading("lucro", text="Lucro")
    #Indicando o tamanho de cada coluna
    tabela_estoque.column("nome", width=100)
    tabela_estoque.column("quantidade", width=80)
    tabela_estoque.column("preco", width=80)
    tabela_estoque.column("preco_custo", width=100)
    tabela_estoque.column("codigo", width=100)
    tabela_estoque.column("markup", width=80)
    tabela_estoque.column("lucro", width=80)

    #A lista propriamente dita
    for produto in produtos:
        nome, quantidade, preco, preco_custo, codigo = produto
        markup = (preco - preco_custo) / preco_custo if preco_custo else 0
        lucro = preco - preco_custo
        tabela_estoque.insert("", "end", values=(nome, quantidade, preco, preco_custo, codigo, f"{markup:.2f}", f"{lucro:.2f}"))

    tabela_estoque.pack(fill="both", expand=True)

#Função para remover da lista
def remover_produto():
    #Janela
    remover_janela = Toplevel(root)
    remover_janela.title("Remover Produto")

    tk.Label(remover_janela, text="Digite o nome ou o código de barras do produto.").pack()
    entrada_busca = tk.Entry(remover_janela)
    entrada_busca.pack()

    #Buscar produtos no banco de dados
    def buscar_produtos():
        termo_busca = entrada_busca.get()
        conexao = sqlite3.connect("controle_estoque.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM produto WHERE nome LIKE ? OR codigo LIKE ?",
                       (f"%{termo_busca}%", f"%{termo_busca}%"))
        resultados = cursor.fetchall()
        conexao.close()

        #Lista dos produtos compativeis
        tabela_resultados = ttk.Treeview(remover_janela, columns=("Nome", "Quantidade", "Preço", "Custo", "Código"), show="headings")
        tabela_resultados.heading("Nome", text="Nome")
        tabela_resultados.heading("Quantidade", text="Quantidade")
        tabela_resultados.heading("Preço", text="Preço")
        tabela_resultados.heading("Custo", text="Preço de custo")
        tabela_resultados.heading("Código", text="Código de barras")

        for produto in resultados:
            tabela_resultados.insert("", "end", values=produto)
        tabela_resultados.pack()

        #Botão remover
        def confirmar_remocao():
            selecionado = tabela_resultados.focus()
            if not selecionado:
                messagebox.showwarning("Seleção", "Selecione um produto para remover")
                return

            item = tabela_resultados.item(selecionado)
            produto_id = item['values'][0] #ID do produto

            conexao = sqlite3.connect("controle_estoque.db")
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM produto WHERE id = ?", (produto_id,))
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Remoção", "Produto removido")
            tabela_resultados.delete(selecionado)

        #Botão de confirmação e de cancelar
        tk.Button(remover_janela, text="Remover", command=confirmar_remocao).pack()
        tk.Button(remover_janela, text="Cancelar", command=remover_janela.destroy).pack()

    #Botão buscar
    tk.Button(remover_janela, text="Buscar", command=buscar_produtos).pack()

#Frame botões lista estoque e remover produto
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

botao_remover = tk.Button(frame_botoes, text="Remover produto", command=remover_produto)
botao_estoque = tk.Button(frame_botoes, text="Visualizar estoque", command=mostrar_estoque)

botao_estoque.pack(side="left", padx=5)
botao_remover.pack(side="right", padx=5)

#Interface loop
root.mainloop()
