import easyocr
import pandas as pd
import os
import cv2
import numpy as np
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PASTA_ENTRADA = os.path.join(BASE_DIR, "..", "nome_destrinchado")
PASTA_SAIDA   = os.path.join(BASE_DIR, "..", "nome_pokemon_preprocessado")

if not os.path.exists(PASTA_SAIDA):
    os.makedirs(PASTA_SAIDA)

reader = easyocr.Reader(['en'], gpu=False)

def tratar_imagem(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    return thresh

def processar_ocr():
    resultados = []
    
    print(f"Iniciando busca recursiva em: {PASTA_ENTRADA}")

    for raiz, diretorios, arquivos in os.walk(PASTA_ENTRADA):
        for nome_arquivo in arquivos:
            if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
                
                caminho_img = os.path.join(raiz, nome_arquivo)
                img = cv2.imread(caminho_img)
                
                if img is None: continue

                img_limpa = tratar_imagem(img)
                
                nome_pasta_pai = os.path.basename(raiz)
                caminho_save = os.path.join(PASTA_SAIDA, f"limpa_{nome_pasta_pai}_{nome_arquivo}")
                cv2.imwrite(caminho_save, img_limpa)
                
                resultado = reader.readtext(
                    img_limpa, 
                    detail=0, 
                    paragraph=True,
                    allowlist='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
                )
                
                if resultado:
                    nome_extraido = " ".join(resultado).strip()
                    resultados.append({"arquivo": nome_arquivo, "pasta": nome_pasta_pai, "nome": nome_extraido})
                    print(f"[OK] {nome_pasta_pai}/{nome_arquivo} -> {nome_extraido}")
                else:
                    print(f"[!] {nome_arquivo} - Texto não encontrado.")

   

if __name__ == "__main__":
    processar_ocr()