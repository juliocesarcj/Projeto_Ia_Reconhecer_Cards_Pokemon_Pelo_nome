import os
import cv2
import csv
import re
import easyocr
import pandas as pd
from rapidfuzz import process, fuzz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_RECORTES  = os.path.join(BASE_DIR, "..", "nome_pokemon_preprocessado")
CSV_SAIDA  = os.path.join(BASE_DIR, "..", "csv/nomes_pokemon.csv")
DATASET_POKEMON  = os.path.join(BASE_DIR, "..", "dataset/All_Pokemon.csv")

reader = easyocr.Reader(["en"], gpu=False)

df = pd.read_csv(DATASET_POKEMON)

for col in ["Name", "name", "pokemon", "identifier"]:
    if col in df.columns:
        COLUNA_NOME = col
        break
else:
    raise ValueError("Coluna de nome não encontrada no CSV")

POKEMONS = df[COLUNA_NOME].astype(str).tolist()
POKEMONS_NORM = [p.lower() for p in POKEMONS]

def limpar_nome(texto):
    return re.sub(r"[^A-Za-zÀ-ÿ ]", "", texto).strip()

def corrigir_com_dataset(texto, limite=70):
    if not texto:
        return "nao legivel"

    melhor, score, idx = process.extractOne(
        texto.lower(),
        POKEMONS_NORM,
        scorer=fuzz.WRatio
    )

    return POKEMONS[idx] if score >= limite else texto

dados = []

for arquivo in os.listdir(PASTA_RECORTES):
    if not arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    caminho = os.path.join(PASTA_RECORTES, arquivo)
    img = cv2.imread(caminho)

    if img is None:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(3.0, (8, 8))
    gray = clahe.apply(gray)

    gray = cv2.fastNlMeansDenoising(gray, None, 12, 7, 21)

    blur = cv2.GaussianBlur(gray, (0, 0), 1.0)
    gray = cv2.addWeighted(gray, 1.3, blur, -0.4, 0)

    gray = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 5
    )

    resultados = reader.readtext(
        gray,
        detail=1,
        decoder="beamsearch",
        allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀ-ÿ "
    )

    if resultados:
        melhor = max(resultados, key=lambda x: x[2])
        nome_final = corrigir_com_dataset(limpar_nome(melhor[1]))
    else:
        nome_final = "nao legivel"

    dados.append([nome_final])
    print(f"{arquivo} -> {nome_final}")

with open(CSV_SAIDA, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["pokemon"])
    writer.writerows(dados)

print(f"\nCSV gerado em: {CSV_SAIDA}")
