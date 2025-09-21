import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
import easyocr
from transformers import pipeline
import json

# ==========================
# Configurações iniciais
# ==========================
ocr = easyocr.Reader(['pt'])  # OCR em português

# LLM gratuito via Hugging Face
llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    tokenizer="google/flan-t5-large"
)

# ==========================
# Função para processar PDF ou imagem
# ==========================
def processar_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("PDF e imagens", "*.pdf *.png *.jpg *.jpeg")])
    if not caminho:
        return

    texto_extraido = ""

    if caminho.lower().endswith(".pdf"):
        # Converter PDF em imagens
        pages = convert_from_path(caminho)
        for i, page in enumerate(pages):
            page_path = f"pagina_{i}.png"
            page.save(page_path, "PNG")
            resultado = ocr.readtext(page_path)
            for (_, txt, _) in resultado:
                texto_extraido += txt + " "
            texto_extraido += "\n--- FIM DA PÁGINA ---\n"
    else:
        # Imagem direta
        resultado = ocr.readtext(caminho)
        for (_, txt, _) in resultado:
            texto_extraido += txt + " "

    # Gerar JSON via LLM
    json_final = gerar_json(texto_extraido)

    # Salvar arquivo
    salvar_caminho = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
    if salvar_caminho:
        with open(salvar_caminho, "w", encoding="utf-8") as f:
            json.dump(json_final, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Sucesso", f"JSON salvo em:\n{salvar_caminho}")
    else:
        messagebox.showwarning("Cancelado", "Salvamento cancelado")

# ==========================
# Função para gerar JSON usando LLM
# ==========================
def gerar_json(texto):
    prompt = f"""
Você é um assistente que organiza textos de documentos escaneados.
Extraia as informações relevantes e entregue em JSON com os seguintes campos:
- titulo
- data
- nomes
- enderecos
- valores
- outros

Texto do documento:
{texto}

JSON:
"""
    resposta = llm(prompt, max_length=1024)[0]['generated_text']

    # Extrair JSON válido
    inicio = resposta.find("{")
    fim = resposta.rfind("}") + 1
    json_texto = resposta[inicio:fim]

    try:
        return json.loads(json_texto)
    except:
        return {"erro": "Não foi possível parsear o JSON"}

# ==========================
# Interface gráfica Tkinter
# ==========================
root = tk.Tk()
root.title("PDF/Imagem → JSON")

root.geometry("400x200")
root.resizable(False, False)

tk.Label(root, text="Extrair informações de PDF ou Imagem", font=("Arial", 14)).pack(pady=20)
tk.Button(root, text="Selecionar Arquivo e Processar", command=processar_arquivo, width=30, height=2).pack(pady=20)

root.mainloop()