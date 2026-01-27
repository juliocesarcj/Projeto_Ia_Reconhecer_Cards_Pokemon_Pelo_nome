import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_NOMES = os.path.join(BASE_DIR, "..", "csv/nomes_pokemon.csv")
CSV_ALL   = os.path.join(BASE_DIR, "..", "dataset/All_Pokemon.csv")
CSV_SAIDA = os.path.join(BASE_DIR, "..", "csv/tipados.csv")

nomes = pd.read_csv(CSV_NOMES)
all_pokemon = pd.read_csv(CSV_ALL)

nomes["pokemon"] = (
    nomes["pokemon"]
    .astype(str)
    .str.strip()
    .str.lower()
)

all_pokemon["Name"] = (
    all_pokemon["Name"]
    .astype(str)
    .str.strip()
    .str.lower()
)

resultado = nomes.merge(
    all_pokemon,
    left_on="pokemon",
    right_on="Name",
    how="left"
)

resultado_final = resultado[[
    "pokemon",
    "Type 1",
    "Type 2"
]]

resultado_final.to_csv(CSV_SAIDA, index=False, encoding="utf-8")

print(f"CSV final gerado em: {CSV_SAIDA}")