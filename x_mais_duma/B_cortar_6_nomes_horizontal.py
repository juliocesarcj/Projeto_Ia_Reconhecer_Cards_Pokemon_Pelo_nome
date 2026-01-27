import cv2
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ENTRADA = os.path.join(BASE_DIR,"..", "nome_recortado")
PASTA_SAIDA   = os.path.join(BASE_DIR, "..","nome")

QTDE_NOMES = 6

BASE_X = 0.00
BASE_Y = 0.09

NOME_LARGURA = 1.0
NOME_ALTURA  = 1.1

ESPACO_ENTRE = 0.06

DEBUG = True
PASTA_DEBUG = os.path.join(BASE_DIR, "..", "debug_nomes")

os.makedirs(PASTA_SAIDA, exist_ok=True)
os.makedirs(PASTA_DEBUG, exist_ok=True)

for arquivo in os.listdir(PASTA_ENTRADA):
    if not arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    img = cv2.imread(os.path.join(PASTA_ENTRADA, arquivo))
    if img is None:
        continue

    if img.shape[0] > img.shape[1]:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    altura, largura, _ = img.shape
    base_nome = os.path.splitext(arquivo)[0]
    img_debug = img.copy()

    for i in range(QTDE_NOMES):
        x1 = int(largura * (BASE_X + i * (NOME_LARGURA + ESPACO_ENTRE)))
        x2 = int(largura * (BASE_X + i * (NOME_LARGURA + ESPACO_ENTRE) + NOME_LARGURA))

        y1 = int(altura * BASE_Y)
        y2 = int(altura * (BASE_Y + NOME_ALTURA))

        x1 = max(0, min(largura, x1))
        x2 = max(0, min(largura, x2))
        y1 = max(0, min(altura, y1))
        y2 = max(0, min(altura, y2))

        if x2 <= x1 or y2 <= y1:
            continue

        recorte = img[y1:y2, x1:x2]
        nome_saida = f"{base_nome}_nome_{i+1}.png"
        cv2.imwrite(os.path.join(PASTA_SAIDA, nome_saida), recorte)

        if DEBUG:
            cv2.rectangle(img_debug, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                img_debug,
                str(i+1),
                (x1 + 5, y1 + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )

    if DEBUG:
        cv2.imwrite(
            os.path.join(PASTA_DEBUG, f"{base_nome}_debug.png"),
            img_debug
        )

print("Cortes realizados.")
