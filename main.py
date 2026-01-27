import subprocess
import os
import sys

# Pasta onde este main.py está (raiz: pokemon)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_script(path):
    """Executa o script usando o mesmo interpretador Python (.venv)."""
    python_exe = sys.executable

    print(f"\nExecutando: {os.path.basename(path)} ---")
    try:
        subprocess.run([python_exe, path], check=True)
        print(f"Sucesso: {os.path.basename(path)}")
    except subprocess.CalledProcessError:
        print(f"\n ERRO ao executar:\n{path}")
        print("Pipeline interrompido para evitar processamento incorreto.")
        sys.exit(1)


def main():
    # Etapas do pipeline (tudo relativo à pasta pokemon)
    etapas = {
        "PRIMEIRO": [
            os.path.join(BASE_DIR, "z_uma", "A_corta.py"),
            os.path.join(BASE_DIR, "x_mais_duma", "A_corta6nomes.py"),
            os.path.join(BASE_DIR, "x_mais_duma", "B_cortar_6_nomes_horizontal.py"),
            os.path.join(BASE_DIR, "x_mais_duma", "C_clivar.py"),
            os.path.join(BASE_DIR, "y_cut_failed_cards", "A_cut_failed_cards.py"),
        ],
        "SEGUNDO": [
            os.path.join(BASE_DIR, "y_cut_failed_cards", "B_cards_fail.py"),
        ],
        "TERCEIRO": [
            os.path.join(BASE_DIR, "z_uma", "B_proeprocess.py"),
        ],
        "QUARTO": [
            os.path.join(BASE_DIR, "x_mais_duma", "E_ler_nome.py"),
        ],
        "QUINTO": [
            os.path.join(BASE_DIR, "z_uma", "D_tipos.py"),
        ],
    }

    print("=== INICIANDO PIPELINE POKEMON 2026 ===")

    for etapa, scripts in etapas.items():
        print("\n###############################")
        print(f"       ETAPA: {etapa}")
        print("###############################")

        for script_path in scripts:
            if not os.path.exists(script_path):
                print(f"\n ERRO CRÍTICO: Arquivo não encontrado:\n{script_path}")
                sys.exit(1)

            run_script(script_path)

    print("\nTodas as 5 etapas foram concluídas com êxito!")


if __name__ == "__main__":
    main()
