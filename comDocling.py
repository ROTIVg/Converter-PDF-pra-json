import tkinter as tk
from tkinter import filedialog, messagebox
from docling import Document
import json

# ==========================
# Função para processar arquivo
# ==========================
def processar_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("PDF e imagens", "*.pdf *.png *.jpg *.jpeg")])
    if not caminho:
        return

    try:
        # Criar objeto Docling
        doc = Document(file_path=caminho)

        # Extrair conteúdo do documento (OCR incluído)
        doc.extract()

        # Converter em JSON
        json_saida = doc.to_json()

        # Salvar JSON em arquivo
        salvar_caminho = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if salvar_caminho:
            with open(salvar_caminho, "w", encoding="utf-8") as f:
                f.write(json_saida)
            messagebox.showinfo("Sucesso", f"JSON salvo em:\n{salvar_caminho}")
        else:
            messagebox.showwarning("Cancelado", "Salvamento cancelado")

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível processar o arquivo.\nErro: {e}")

# ==========================
# Interface gráfica Tkinter
# ==========================
root = tk.Tk()
root.title("Docling PDF/Imagem → JSON")

root.geometry("450x200")
root.resizable(False, False)

tk.Label(root, text="Extrair informações de PDF ou Imagem", font=("Arial", 14)).pack(pady=20)
tk.Button(root, text="Selecionar Arquivo e Gerar JSON", command=processar_arquivo, width=30, height=2).pack(pady=20)

root.mainloop()
