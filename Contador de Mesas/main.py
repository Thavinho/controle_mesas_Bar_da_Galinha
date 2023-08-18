import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import os
import openpyxl
from datetime import date

def exibir_nova_adicao():
    nova_adicao_janela = tk.Toplevel(root)
    nova_adicao_janela.title("Nova Adição")
    nova_adicao_janela.geometry("500x500")

    nome_label = ttk.Label(nova_adicao_janela, text="Nome:")
    nome_label.pack(padx=10, pady=5)
    nome_entry = ttk.Entry(nova_adicao_janela)
    nome_entry.pack(padx=10, pady=5)

    mesa_label = ttk.Label(nova_adicao_janela, text="Mesa:")
    mesa_label.pack(padx=10, pady=5)
    
    mesas_disponiveis = list(range(1, 81))
    conn = sqlite3.connect("Mesas_Bar_da_Galinha.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Mesa FROM InformacoesCliente")
    mesas_ocupadas = cursor.fetchall()
    conn.close()
    mesas_disponiveis = [mesa for mesa in mesas_disponiveis if (str(mesa),) not in mesas_ocupadas]
    
    mesa_combobox = ttk.Combobox(nova_adicao_janela, values=mesas_disponiveis, state="readonly")
    mesa_combobox.pack(padx=10, pady=5)

    cadeira_extra_label = ttk.Label(nova_adicao_janela, text="Cadeira Extra:")
    cadeira_extra_label.pack(padx=10, pady=5)
    
    opcoes_cadeira_extra = ["Sem cadeira extra", "+1", "+2"]
    cadeira_extra_combobox = ttk.Combobox(nova_adicao_janela, values=opcoes_cadeira_extra, state="readonly")
    cadeira_extra_combobox.pack(padx=10, pady=5)
    
    pago_label = ttk.Label(nova_adicao_janela, text="Pago:")
    pago_label.pack(padx=10, pady=5)
    pago_combobox = ttk.Combobox(nova_adicao_janela, values=["Sim", "Não"], state="readonly")
    pago_combobox.pack(padx=10, pady=5)

    def adicionar_dados():
        nome = nome_entry.get()
        mesa = mesa_combobox.get()
        cadeira_extra = cadeira_extra_combobox.get()
        pago = pago_combobox.get()
        conn = sqlite3.connect("Mesas_Bar_da_Galinha.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO InformacoesCliente (Nome, Mesa, CadeiraExtra, Pago) VALUES (?, ?, ?, ?)",
                    (nome, mesa, cadeira_extra, pago))
        conn.commit()
        conn.close()
        informacoes_label = ttk.Label(nova_adicao_janela, text="Dados inseridos com sucesso!")
        informacoes_label.pack(padx=10, pady=10)
        
        # Atualizar a página de edições
        nova_adicao_janela.destroy()
        exibir_editar_entradas()

    adicionar_button = ttk.Button(nova_adicao_janela, text="Adicionar", command=adicionar_dados)
    adicionar_button.pack(padx=10, pady=10)

def exibir_editar_entradas():
    def excluir_entrada(id_, janela):
        resposta = messagebox.askyesno("Confirmação de Exclusão", "Tem certeza que deseja excluir esta entrada?")
        if resposta:
            conn = sqlite3.connect("Mesas_Bar_da_Galinha.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM InformacoesCliente WHERE ID=?", (id_,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Exclusão", "Entrada excluída com sucesso.")
            janela.destroy()
            exibir_editar_entradas()

    editar_entradas_janela = tk.Toplevel(root)
    editar_entradas_janela.title("Editar Entrada")
    editar_entradas_janela.geometry("500x500")

    conn = sqlite3.connect("Mesas_Bar_da_Galinha.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM InformacoesCliente ORDER BY Mesa")
    dados = cursor.fetchall()
    conn.close()

    if not dados:
        messagebox.showinfo("Nenhuma entrada", "Não existe nenhuma entrada no banco de dados.")
        editar_entradas_janela.destroy()
        return

    for linha in dados:
        id_, nome, mesa, cadeira_extra, pago = linha
        label = tk.Label(editar_entradas_janela, text=f"Mesa: {mesa}, Nome: {nome}")
        label.pack(padx=10, pady=5)
        frame_botoes = ttk.Frame(editar_entradas_janela)
        frame_botoes.pack(padx=10, pady=5)
        editar_button = ttk.Button(frame_botoes, text="Editar",
                                   command=lambda id_=id_, mesa=mesa, nome=nome, cadeira_extra=cadeira_extra, pago=pago: exibir_dados_para_edicao(editar_entradas_janela, id_, mesa, nome, cadeira_extra, pago))
        editar_button.pack(side="left", padx=5)
        excluir_button = ttk.Button(frame_botoes, text="Excluir",
                                    command=lambda id_=id_, janela=editar_entradas_janela: excluir_entrada(id_, janela))
        excluir_button.pack(side="left", padx=5)

    ok_button = ttk.Button(editar_entradas_janela, text="OK", command=editar_entradas_janela.destroy)
    ok_button.pack(pady=10) 

def exibir_dados_para_edicao(editar_entradas_janela, id_, mesa, nome, cadeira_extra, pago):
    dados_para_edicao_janela = tk.Toplevel(editar_entradas_janela)
    dados_para_edicao_janela.title("Editar Dados")
    dados_para_edicao_janela.geometry("400x300")

    nome_label = ttk.Label(dados_para_edicao_janela, text="Nome:")
    nome_label.pack(padx=10, pady=5)
    nome_entry = ttk.Entry(dados_para_edicao_janela, width=30)
    nome_entry.pack(padx=10, pady=5)
    nome_entry.insert(0, nome)

    mesa_label = ttk.Label(dados_para_edicao_janela, text="Mesa:")
    mesa_label.pack(padx=10, pady=5)
    mesa_entry = ttk.Entry(dados_para_edicao_janela, width=30, state="readonly")
    mesa_entry.pack(padx=10, pady=5)
    mesa_entry.insert(0, mesa)

    cadeira_extra_label = ttk.Label(dados_para_edicao_janela, text="Cadeira Extra:")
    cadeira_extra_label.pack(padx=10, pady=5)
    
    opcoes_cadeira_extra = ["Sem cadeira extra", "+1", "+2"]
    cadeira_extra_combobox = ttk.Combobox(dados_para_edicao_janela, values=opcoes_cadeira_extra, state="readonly")
    cadeira_extra_combobox.pack(padx=10, pady=5)
    cadeira_extra_combobox.set(cadeira_extra)

    pago_label = ttk.Label(dados_para_edicao_janela, text="Pago:")
    pago_label.pack(padx=10, pady=5)
    pago_combobox = ttk.Combobox(dados_para_edicao_janela, values=["Sim", "Não"], state="readonly")
    pago_combobox.pack(padx=10, pady=5)
    pago_combobox.set(pago)

    def salvar_edicao():
        novo_nome = nome_entry.get()
        novo_cadeira_extra = cadeira_extra_combobox.get()
        novo_pago = pago_combobox.get()
        conn = sqlite3.connect("Mesas_Bar_da_Galinha.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE InformacoesCliente SET Nome=?, CadeiraExtra=?, Pago=? WHERE ID=?", (novo_nome, novo_cadeira_extra, novo_pago, id_))
        conn.commit()
        conn.close()
        messagebox.showinfo("Edição", "Dados atualizados com sucesso!")
        dados_para_edicao_janela.destroy()
        exibir_editar_entradas()

    salvar_button = ttk.Button(dados_para_edicao_janela, text="Salvar", command=salvar_edicao)
    salvar_button.pack(padx=10, pady=10)
    
def exibir_exportar():
    exportar_janela = tk.Toplevel(root)
    exportar_janela.title("Exportar Dados")
    exportar_janela.geometry("300x150")

    def exportar_dados():
        senha_exportar = simpledialog.askstring("Senha de Exportação", "Digite a senha para exportar os dados:")
        if senha_exportar == "bdg2023":
            data_atual = date.today().strftime("%Y-%m-%d")
            pasta_exportacao = f"Export_{data_atual}"
            os.makedirs(pasta_exportacao, exist_ok=True)
            conn = sqlite3.connect("Mesas_Bar_da_Galinha.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM InformacoesCliente ORDER BY Mesa")
            dados = cursor.fetchall()
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Dados Cliente"
            ws.append(["ID", "Nome", "Mesa", "Cadeira Extra", "Pago"])
            for linha in dados:
                ws.append(linha)
            arquivo_excel = os.path.join(pasta_exportacao, "dados.xlsx")
            wb.save(arquivo_excel)
            conn.close()
            messagebox.showinfo("Exportar", "Dados exportados com sucesso!")
            exportar_janela.destroy()
        else:
            messagebox.showerror("Erro de Senha", "Senha incorreta!")

    exportar_label = ttk.Label(exportar_janela, text="Clique no botão abaixo para exportar os dados para Excel.")
    exportar_label.pack(padx=10, pady=10)

    exportar_button = ttk.Button(exportar_janela, text="Exportar", command=exportar_dados)
    exportar_button.pack(padx=10, pady=10)

root = tk.Tk()
root.title("Reservas Bar da Galinha")
root.geometry("500x500")

conn = sqlite3.connect("Mesas_Bar_da_Galinha.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS InformacoesCliente (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT,
            Mesa TEXT,
            CadeiraExtra TEXT,
            Pago TEXT
            )''')
conn.commit()
conn.close()

novo_adicao_button = ttk.Button(root, text="Nova Adição", command=exibir_nova_adicao)
novo_adicao_button.pack(padx=10, pady=5)

editar_entradas_button = ttk.Button(root, text="Editar Entrada", command=exibir_editar_entradas)
editar_entradas_button.pack(padx=10, pady=5)

exportar_button = ttk.Button(root, text="Exportar", command=exibir_exportar)
exportar_button.pack(padx=10, pady=5)

root.mainloop()
