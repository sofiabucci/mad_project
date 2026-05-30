"""
ITEM 2c - Resolução com Google OR-Tools (MIP)
Baseado no código da professora partsRects.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from instancia import INSTANCIA
from ortools.linear_solver import pywraplp
import time

def resolver_com_codigo_professora():
    print("\n" + "=" * 70)
    print("ITEM 2c - GOOGLE OR-TOOLS (MIP) - Código da Professora")
    print("=" * 70)
    
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver SCIP não disponível")
        return None

    # Variáveis
    x = {i: solver.IntVar(0, 1, f'x_{i}') for i in range(1, 9)}
    
    # Restrições (conforme código da professora)
    solver.Add(x[8] >= 1)                                    # R10
    solver.Add(x[8] + x[7] >= 1)                             # R8
    solver.Add(x[7] + x[6] + x[4] + x[5] >= 1)              # R4
    solver.Add(x[7] + x[6] + x[8] >= 1)                     # R7
    solver.Add(x[3] + x[4] >= 1)                            # R3
    solver.Add(x[2] + x[1] >= 1)                            # R2
    solver.Add(x[5] + x[4] + x[3] + x[2] >= 1)              # R4 (redundante)
    solver.Add(x[5] + x[6] >= 1)                            # R5
    solver.Add(x[1] + x[3] + x[2] >= 1)                     # R9
    solver.Add(x[1] >= 1)                                   # R1
    
    # Objetivo
    objective = solver.Objective()
    for i in range(1, 9):
        objective.SetCoefficient(x[i], 1)
    objective.SetMinimization()

    # Resolver
    inicio = time.time()
    status = solver.Solve()
    tempo = (time.time() - inicio) * 1000

    if status == pywraplp.Solver.OPTIMAL:
        custo = int(objective.Value())
        guardas = [i for i in range(1, 9) if x[i].solution_value() > 0.5]
        print(f"\n✓ Solução ótima encontrada!")
        print(f"  • Tempo: {tempo:.3f} ms")
        print(f"  • Guardas: {guardas}")
        print(f"  • Número: {custo}")
        return custo, guardas
    else:
        print("✗ Nenhuma solução ótima encontrada.")
        return None, None

def main():
    resolver_com_codigo_professora()

if __name__ == "__main__":
    main()