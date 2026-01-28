from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PASTA_ENTRADA = os.path.join(BASE_DIR, "..", "fail_cards")
PASTA_SAIDA   = os.path.join(BASE_DIR, "..", "nome_fail_retangulo_good")

os.makedirs(PASTA_SAIDA, exist_ok=True)

CORTES = [
    {"x": 0.0, "y": 0.01, "w": 1.0, "h": 0.02},
    {"x": 0.0, "y": 0.3, "w": 1.0, "h": 0.03},
    {"x": 0.0, "y": 0.6, "w": 1.0, "h": 0.03}, 
]

for arquivo in os.listdir(PASTA_ENTRADA):
    if not arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
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
        y1 = int(altura * c["y"])
        x2 = int(largura * (c["x"] + c["w"]))
        y2 = int(altura * (c["y"] + c["h"]))

        corte = img.crop((x1, y1, x2, y2))
        
        saida = os.path.join(PASTA_SAIDA, f"{os.path.splitext(arquivo)[0]}_horizontal_{i}.png")
        corte.save(saida)
        print(f"{arquivo}corte horizontal {i} salvo")

print("Finalizado.")
