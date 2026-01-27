from PIL import Image
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ENTRADA = os.path.join(BASE_DIR, "..", "nome")
PASTA_SAIDA   = os.path.join(BASE_DIR, "..", "nome_destrinchado")

os.makedirs(PASTA_SAIDA, exist_ok=True)

CORTES = [
    {"x": 0.124, "y": 0.30, "w": 0.06, "h": 0.90},
    {"x": 0.275, "y": 0.30, "w": 0.06, "h": 0.90},
    {"x": 0.425, "y": 0.30, "w": 0.06, "h": 0.90},
    {"x": 0.575, "y": 0.30, "w": 0.06, "h": 0.90},
    {"x": 0.737, "y": 0.25, "w": 0.06, "h": 0.90},
    {"x": 0.875, "y": 0.30, "w": 0.06, "h": 0.90},
]

for arquivo in os.listdir(PASTA_ENTRADA):
    if not arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    caminho = os.path.join(PASTA_ENTRADA, arquivo)

    try:
        img = Image.open(caminho)
    except Exception as e:
        print(f"{arquivo}erro ao abrir: {e}")
        continue

    largura, altura = img.size

    for i, c in enumerate(CORTES):
        x1 = int(largura * c["x"])
        y1 = int(altura  * c["y"])
        x2 = x1 + int(largura * c["w"])
        y2 = y1 + int(altura  * c["h"])

        if x2 > largura: x2 = largura
        if y2 > altura:  y2 = altura

        corte = img.crop((x1, y1, x2, y2))

        saida = os.path.join(
            PASTA_SAIDA,
            f"{os.path.splitext(arquivo)[0]}_corte_{i}.png"
        )

        corte.save(saida)
        print(f"{arquivo} -> corte {i} salvo")

print("Finalizado.")
