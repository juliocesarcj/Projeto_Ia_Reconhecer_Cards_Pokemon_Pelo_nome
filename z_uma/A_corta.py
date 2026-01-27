from PIL import Image
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PASTA_CARTAS = os.path.join(BASE_DIR, "..", "cartas")
PASTA_SAIDA  = os.path.join(BASE_DIR, "..", "nome_destrinchado")

os.makedirs(PASTA_SAIDA, exist_ok=True)

AJUSTE_TOPO = 0.00       
AJUSTE_BASE = 0.02       
DESLOC_X    = 0.00       
DESLOC_Y    = 0.00       

NOME_X1 = 0.18
NOME_X2 = 0.70
NOME_Y1 = 0.00
NOME_Y2 = 0.10 

for arquivo in os.listdir(PASTA_CARTAS):
    if not arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    caminho = os.path.join(PASTA_CARTAS, arquivo)

    try:
        img = Image.open(caminho)
    except Exception as e:
        print(f"{arquivo}erro ao abrir: {e}")
        continue

    largura, altura = img.size

    topo_global  = int(altura * AJUSTE_TOPO) + int(altura * DESLOC_Y)
    baixo_global = int(altura * (1 - AJUSTE_BASE)) + int(altura * DESLOC_Y)
    
    esquerda_global = int(largura * DESLOC_X)
    direita_global  = largura + int(largura * DESLOC_X)

    carta = img.crop((esquerda_global, topo_global, direita_global, baixo_global))
    w_cart, h_cart = carta.size

    nome = carta.crop((
        int(w_cart * NOME_X1),
        int(h_cart * NOME_Y1),
        int(w_cart * NOME_X2),
        int(h_cart * NOME_Y2)
    ))

    saida = os.path.join(
        PASTA_SAIDA,
        f"{os.path.splitext(arquivo)[0]}_nome.png"
    )

    nome.save(saida)
    print(f"{arquivo}nomes salvos")

print("Processo finalizado.")