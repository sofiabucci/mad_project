import subprocess
import sys
import time
from datetime import datetime
import os

# Criar pasta results
os.makedirs("results", exist_ok=True)

def run_and_capture(script_name, description, use_python=True):
    print(f"\n{'='*70}")
    print(f"Executando: {description}")
    print('='*70)
    
    inicio = time.time()
    try:
        if use_python:
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                timeout=30
            )
        else:
            result = subprocess.run(
                script_name.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
        tempo = time.time() - inicio
        
        output = result.stdout + result.stderr
        
        base_name = os.path.basename(script_name).replace('.py', '').replace('.pl', '')
        output_file = f"results/{base_name}.txt"
        
        with open(output_file, "w") as f:
            f.write(f"=== {description} ===\n")
            f.write(f"Tempo: {tempo:.3f}s\n")
            f.write(f"Return code: {result.returncode}\n")
            f.write("="*70 + "\n\n")
            f.write(output)
        
        print(output)
        print(f"\n✓ Resultado guardado em: {output_file}")
        
    except Exception as e:
        print(f"✗ Erro: {e}")

# Scripts
scripts = [
    ("1/greedyS.py", "Item 1 - Estratégias Greedy", True),
    ("2/b_ac3_mac.py", "Item 2b - MAC + AC-3", True),
    ("2/c_ortools.py", "Item 2c - Google OR-Tools", True),
    ("3/prog_dinam.py", "Item 3 - Programação Dinâmica", True),
    ("4/a.py", "Item 4a - Guardas com Cores", True),
    ("4/b.py", "Item 4b - Guardas com Alcance", True),
]

print("="*70)
print("A CORRER TODOS OS MÓDULOS")
print(f"Início: {datetime.now()}")
print("="*70)

for script, desc, use_python in scripts:
    run_and_capture(script, desc, use_python)

print("\n" + "="*70)
print(f"FIM - Resultados guardados em: results/")
print("="*70)