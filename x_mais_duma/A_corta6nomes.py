from PIL import Image
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_CARTAS = os.path.join(BASE_DIR, "..","multiplas_cartas")
PASTA_SAIDA  = os.path.join(BASE_DIR, "..", "nome_recortado")

os.makedirs(PASTA_SAIDA, exist_ok=True)

NUM_CORTES = 3
LARGURA_CORTE = 0.03

POSICOES_X = [
    0.00,
    0.30,
    0.60
]

for arquivo in os.listdir(PASTA_CARTAS):
    if not arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    caminho = os.path.join(PASTA_CARTAS, arquivo)

    try:
        img = Image.open(caminho)
    except Exception as e:
        print(f"{arquivo} erro ao abrir: {e}")
        continue

    largura, altura = img.size
    largura_corte_px = int(largura * LARGURA_CORTE)

    for i in range(NUM_CORTES):
        esquerda = int(largura * POSICOES_X[i])
        direita  = esquerda + largura_corte_px

        if direita > largura:
            direita = largura

        corte = img.crop((esquerda, 0, direita, altura))

        saida = os.path.join(
            PASTA_SAIDA,
            f"{os.path.splitext(arquivo)[0]}_vertical_{i}.png"
        )

        corte.save(saida)
        print(f"{arquivo}  {i} salvo")

print("Finalizado.")
