from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ENTRADA = os.path.join(BASE_DIR, "..", "nome_fail_retangulo_good")
PASTA_SAIDA  = os.path.join(BASE_DIR, "..", "nome_destrinchado")

os.makedirs(PASTA_SAIDA, exist_ok=True)


CORTES = [
    {"x": 0.15, "y": 0.09, "w": 0.17, "h": 0.9},  
    {"x": 0.45, "y": 0.09, "w": 0.17, "h": 0.9},  
    {"x": 0.75, "y": 0.09, "w": 0.17, "h": 0.9},  
]

for arquivo in os.listdir(PASTA_ENTRADA):
    if not arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    caminho = os.path.join(PASTA_ENTRADA, arquivo)
    
    try:
        with Image.open(caminho) as img:
            larg_total, alt_total = img.size

            for i, c in enumerate(CORTES):
                x1 = int(larg_total * c["x"])
                y1 = int(alt_total * c["y"])
                x2 = int(larg_total * (c["x"] + c["w"]))
                y2 = int(alt_total * (c["y"] + c["h"]))

                x2 = min(x2, larg_total)
                y2 = min(y2, alt_total)

                corte = img.crop((x1, y1, x2, y2))

                nome_saida = f"{os.path.splitext(arquivo)[0]}_corte_{i+1}.png"
                corte.save(os.path.join(PASTA_SAIDA, nome_saida))
                
                print(f"{arquivo} -> corte {i+1} salvo")

    except Exception as e:
        print(f"Erro ao processar {arquivo}: {e}")

print("Finalizado.")