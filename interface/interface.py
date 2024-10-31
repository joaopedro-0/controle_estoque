import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
import sqlite3
from tkinter import messagebox, Toplevel, ttk
import tkinter as tk
from tkinter import messagebox
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
    estoque_janela.geometry("700x500")

    #Campo de busca
    tk.Label(estoque_janela, text="Buscar produto").pack(pady=5)
    entrada_busca = tk.Entry(estoque_janela)
    entrada_busca.pack(pady=5)
    entrada_busca.bind("<KeyRelease>", lambda event: atualizar_lista_estoque())

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
    tabela_estoque.pack(fill="both", expand=True)

    #Indicando o tamanho de cada coluna
    tabela_estoque.column("nome", width=100)
    tabela_estoque.column("quantidade", width=80)
    tabela_estoque.column("preco", width=80)
    tabela_estoque.column("preco_custo", width=100)
    tabela_estoque.column("codigo", width=100)
    tabela_estoque.column("markup", width=80)
    tabela_estoque.column("lucro", width=80)

    #Atualizar a lista com busca
    def atualizar_lista_estoque():
        termo_busca = entrada_busca.get()
        conexao = sqlite3.connect("controle_estoque.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, quantidade, preco, preco_custo, codigo FROM produto WHERE nome LIKE ? OR codigo LIKE ?", (f"%{termo_busca}%", f"%{termo_busca}%"))
        produtos_atualizados = cursor.fetchall()
        conexao.close()

        #Limpar lista
        tabela_estoque.delete(*tabela_estoque.get_children())
        for produto in produtos_atualizados:
            nome, quantidade, preco, preco_custo, codigo = produto
            markup = (preco - preco_custo) / (preco_custo if preco_custo else 1)
            lucro = preco - preco_custo
            tabela_estoque.insert("", "end", values=(nome, quantidade, preco, preco_custo, codigo, f"{markup:.2f}", f"{lucro:.2f}"))

    #Editar produto
    def editar_produto():
        selecionado = tabela_estoque.focus()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione um produto para editar")
            return

        item = tabela_estoque.item(selecionado)
        try:
            produto_nome, quantidade, preco, preco_custo, codigo, markup, lucro = item['values']
        except ValueError:
            messagebox.showerror("Erro", "Erro ao desempacotar os valores do produto")
            return

        #Janela de edição
        editar_janela = Toplevel(estoque_janela)
        editar_janela.title("Editar Produto")

        tk.Label(editar_janela, text="Nome:").pack()
        entrada_nome = tk.Entry(editar_janela)
        entrada_nome.insert(0, produto_nome)
        entrada_nome.pack()

        tk.Label(editar_janela, text="Quantidade:").pack()
        entrada_quantidade = tk.Entry(editar_janela)
        entrada_quantidade.insert(0, quantidade)
        entrada_quantidade.pack()

        tk.Label(editar_janela, text="Preço de venda:").pack()
        entrada_preco = tk.Entry(editar_janela)
        entrada_preco.insert(0, preco)
        entrada_preco.pack()

        tk.Label(editar_janela, text="Preço de custo:").pack()
        entrada_preco_custo = tk.Entry(editar_janela)
        entrada_preco_custo.insert(0, preco_custo)
        entrada_preco_custo.pack()

        tk.Label(editar_janela, text="Código de barras:").pack()
        entrada_codigo = tk.Entry(editar_janela)
        entrada_codigo.insert(0, codigo)
        entrada_codigo.pack()

        def salvar_edicao():
            novo_nome = entrada_nome.get()
            nova_quantidade = int(entrada_quantidade.get())
            novo_preco = float(entrada_preco.get().replace(',', '.'))
            novo_preco_custo = float(entrada_preco_custo.get().replace(',', '.'))
            novo_codigo = entrada_codigo.get()

            try:
                nova_quantidade = int(nova_quantidade)
                novo_preco = float(novo_preco)
                novo_preco_custo =float(novo_preco_custo)
            except ValueError:
                messagebox.showerror("Erro", "Certifique-se de que seja valores números")
                return

            try:
                conexao = sqlite3.connect("controle_estoque.db")
                cursor = conexao.cursor()
                cursor.execute("""
                    UPDATE produto SET nome=?, quantidade=?, preco=?, preco_custo=?, codigo=? WHERE codigo=?""",
                               (novo_nome, nova_quantidade, novo_preco, novo_preco_custo, novo_codigo, codigo))
                conexao.commit()
                conexao.close()
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                atualizar_lista_estoque()
                editar_janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar produto: {e}")

        tk.Button(editar_janela, text="Salvar", command=salvar_edicao).pack(pady=5)
        tk.Button(editar_janela, text="Cancelar", command=editar_janela.destroy).pack(pady=5)
    def remover_produto():
        selecionado = tabela_estoque.focus()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione um produto para remover")
            return

        item = tabela_estoque.item(selecionado)
        try:
            produto_codigo = item['values'][4]
        except ValueError:
            messagebox.showerror("Erro", "Erro ao desempacotar os valores do produto")
            return

        #Confirmação
        confirmacao = messagebox.askyesno("Confirmar remoção", "Tem certeza que deseja remover esse produto?")
        if confirmacao:
            try:
                conexao = sqlite3.connect("controle_estoque.db")
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM produto WHERE codigo=?", (produto_codigo,))
                conexao.commit()
                conexao.close()
                messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
                atualizar_lista_estoque()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover produto: {e}")

    tk.Button(estoque_janela, text="Editar produto", command=editar_produto).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(estoque_janela, text="Remover produto", command=remover_produto).pack(side=tk.RIGHT, padx=10, pady=10)


    #A lista propriamente dita
    for produto in produtos:
        nome, quantidade, preco, preco_custo, codigo = produto
        markup = (preco - preco_custo) / preco_custo if preco_custo else 0
        lucro = preco - preco_custo
        tabela_estoque.insert("", "end", values=(nome, quantidade, preco, preco_custo, codigo, f"{markup:.2f}", f"{lucro:.2f}"))

    tabela_estoque.pack(fill="both", expand=True)


#Frame botões lista estoque e remover produto
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

botao_estoque = tk.Button(frame_botoes, text="Visualizar estoque", command=mostrar_estoque)

botao_estoque.pack(side="left", padx=5)

#Interface loop
root.mainloop()
