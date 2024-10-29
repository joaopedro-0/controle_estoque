import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
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

#Interface loop
root.mainloop()
