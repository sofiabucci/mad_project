import subprocess
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()

def print_header(title):
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)

def print_subheader(title):
    print("\n" + "-" * 60)
    print(f" {title}")
    print("-" * 60)

def run_python_script(path, description):
    full_path = BASE_DIR / path
    if not full_path.exists():
        print(f"Ficheiro nao encontrado: {path}")
        return False
    
    print_subheader(description)
    try:
        result = subprocess.run(
            [sys.executable, str(full_path)],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Erro ao executar {path}: {e}")
        return False

def run_prolog_script(path, description):
    full_path = BASE_DIR / path
    if not full_path.exists():
        print(f"Ficheiro nao encontrado: {path}")
        return False
    
    print_subheader(description)
    try:
        result = subprocess.run(
            ["swipl", "-q", "-t", "halt", str(full_path)],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("SWI-Prolog nao encontrado. Instale com: sudo apt-get install swi-prolog")
        return False
    except Exception as e:
        print(f"Erro ao executar {path}: {e}")
        return False

def main():
    print_header("RESOLUCAO DO PROBLEMA DE COBERTURA DE PARTICOES RETANGULARES")
    print(" MAD 2025/2026")
    print(f" Diretorio: {BASE_DIR}")
    
    resultados = []
    
    # ITEM 1 - Estrategias Greedy
    print_header("ITEM 1 - ESTRATEGIAS GREEDY")
    ok = run_python_script("1/greedy.py", "Executando greedy.py")
    resultados.append(("Item 1 - Greedy", ok))
    
    # ITEM 2 - Programacao Inteira e Restricoes
    print_header("ITEM 2 - PROGRAMACAO INTEIRA E RESTRICOES")
    
    ok = run_python_script("2/b_ac3_mac.py", "2b - MAC + AC-3 (Propagacao de Restricoes)")
    resultados.append(("Item 2b - MAC+AC3", ok))
    
    ok = run_python_script("2/c_ortools.py", "2c - Google OR-Tools (CP-SAT e MIP)")
    resultados.append(("Item 2c - OR-Tools", ok))
    
    ok = run_prolog_script("2/c_prolog.pl", "2c - SWI-Prolog (CLPFD)")
    resultados.append(("Item 2c - Prolog", ok))
    
    # ITEM 3 - Programacao Dinamica
    print_header("ITEM 3 - PROGRAMACAO DINAMICA")
    ok = run_python_script("3/prog_dinam.py", "Executando prog_dinam.py")
    resultados.append(("Item 3 - PD", ok))
    
    # ITEM 4 - Extensoes
    print_header("ITEM 4 - EXTENSOES")
    
    ok = run_python_script("4/a.py", "4a - Guardas com Cores")
    resultados.append(("Item 4a - Cores", ok))
    
    ok = run_python_script("4/b.py", "4b - Guardas com Maior Alcance")
    resultados.append(("Item 4b - Alcance", ok))
    
    # RESUMO FINAL
    print_header("RESUMO DE EXECUCAO")
    
    print("\n| Modulo | Status |")
    print("|--------|--------|")
    for nome, status in resultados:
        status_str = "SUCESSO" if status else "FALHA"
        print(f"| {nome} | {status_str} |")
    
    total = len(resultados)
    sucessos = sum(1 for _, s in resultados if s)
    print(f"\nTotal: {sucessos}/{total} modulos executados com sucesso")
    
    print("\n" + "=" * 80)
    print(" FIM DA EXECUCAO")
    print("=" * 80)

if __name__ == "__main__":
    main()