"""
ITEM 2c - Resolução com Google OR-Tools (CP-SAT)
Melhorado a partir do código fornecido pela professora
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.instancia import INSTANCIA
import time

class ORToolsSolver:
    def __init__(self, instancia=None):
        self.instancia = instancia or INSTANCIA
    
    def resolver_cp_sat(self):
        """Resolução com CP-SAT"""
        try:
            from ortools.sat.python import cp_model
        except ImportError:
            print("OR-Tools não instalado. Execute: pip install ortools")
            return None, []
        
        print("\n" + "=" * 70)
        print("ITEM 2c - GOOGLE OR-TOOLS (CP-SAT)")
        print("=" * 70)
        
        model = cp_model.CpModel()
        
        # Variáveis
        x = {v: model.NewBoolVar(f'x_{v}') for v in self.instancia.vertices}
        
        # Restrições (baseadas no código da professora)
        # R1: x1 >= 1
        model.Add(x[1] >= 1)
        # R2: x1 + x2 >= 1
        model.Add(x[1] + x[2] >= 1)
        # R3: x3 + x4 >= 1
        model.Add(x[3] + x[4] >= 1)
        # R4: x2 + x3 + x4 + x5 >= 1
        model.Add(x[2] + x[3] + x[4] + x[5] >= 1)
        # R5: x5 + x6 >= 1
        model.Add(x[5] + x[6] >= 1)
        # R6: x6 + x7 >= 1
        model.Add(x[6] + x[7] >= 1)
        # R7: x6 + x7 + x8 >= 1
        model.Add(x[6] + x[7] + x[8] >= 1)
        # R8: x7 + x8 >= 1
        model.Add(x[7] + x[8] >= 1)
        # R9: x1 + x2 + x3 + x4 + x5 >= 1
        model.Add(x[1] + x[2] + x[3] + x[4] + x[5] >= 1)
        # R10: x8 >= 1
        model.Add(x[8] >= 1)
        
        # Objetivo
        model.Minimize(sum(x[v] for v in self.instancia.vertices))
        
        # Resolver
        inicio = time.time()
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10.0
        status = solver.Solve(model)
        tempo = (time.time() - inicio) * 1000
        
        if status == cp_model.OPTIMAL:
            custo = int(solver.ObjectiveValue())
            solucao = {v for v in self.instancia.vertices if solver.Value(x[v]) == 1}
            print(f"\n✓ Solução ótima encontrada!")
            print(f"  • Tempo: {tempo:.3f} ms")
            print(f"  • Guardas: {sorted(solucao)}")
            print(f"  • Número: {custo}")
            return custo, [solucao]
        else:
            print(f"\n✗ Status: {status}")
            return None, []
    
    def resolver_mip(self):
        """Resolução com MIP (Mixed Integer Programming) - código original da professora"""
        try:
            from ortools.linear_solver import pywraplp
        except ImportError:
            print("MIP não disponível")
            return None, []
        
        print("\n" + "=" * 70)
        print("ITEM 2c - GOOGLE OR-TOOLS (MIP)")
        print("=" * 70)
        
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            print("Solver SCIP não disponível")
            return None, []
        
        # Variáveis
        x = {i: solver.IntVar(0, 1, f'x_{i}') for i in range(1, 9)}
        
        # Restrições (igual ao código da professora)
        solver.Add(x[8] >= 1)
        solver.Add(x[8] + x[7] >= 1)
        solver.Add(x[7] + x[6] + x[4] + x[5] >= 1)
        solver.Add(x[7] + x[6] + x[8] >= 1)
        solver.Add(x[3] + x[4] >= 1)
        solver.Add(x[2] + x[1] >= 1)
        solver.Add(x[5] + x[4] + x[3] + x[2] >= 1)
        solver.Add(x[5] + x[6] >= 1)
        solver.Add(x[1] + x[3] + x[2] >= 1)
        solver.Add(x[1] >= 1)
        
        # Objetivo
        objective = solver.Objective()
        for i in range(1, 9):
            objective.SetCoefficient(x[i], 1)
        objective.SetMinimization()
        
        inicio = time.time()
        status = solver.Solve()
        tempo = (time.time() - inicio) * 1000
        
        if status == pywraplp.Solver.OPTIMAL:
            custo = int(objective.Value())
            solucao = {i for i in range(1, 9) if x[i].solution_value() > 0.5}
            print(f"\n✓ Solução ótima encontrada!")
            print(f"  • Tempo: {tempo:.3f} ms")
            print(f"  • Guardas: {sorted(solucao)}")
            print(f"  • Número: {custo}")
            return custo, [solucao]
        else:
            print(f"\n✗ Nenhuma solução ótima encontrada")
            return None, []
    
    def resolver_todas_solucoes(self):
        """Encontra todas as soluções ótimas"""
        try:
            from ortools.sat.python import cp_model
        except ImportError:
            return None, []
        
        model = cp_model.CpModel()
        
        x = {v: model.NewBoolVar(f'x_{v}') for v in self.instancia.vertices}
        
        # Restrições
        model.Add(x[1] >= 1)
        model.Add(x[1] + x[2] >= 1)
        model.Add(x[3] + x[4] >= 1)
        model.Add(x[2] + x[3] + x[4] + x[5] >= 1)
        model.Add(x[5] + x[6] >= 1)
        model.Add(x[6] + x[7] >= 1)
        model.Add(x[6] + x[7] + x[8] >= 1)
        model.Add(x[7] + x[8] >= 1)
        model.Add(x[1] + x[2] + x[3] + x[4] + x[5] >= 1)
        model.Add(x[8] >= 1)
        
        custo_var = model.NewIntVar(0, self.instancia.num_vertices, 'custo')
        model.Add(custo_var == sum(x[v] for v in self.instancia.vertices))
        model.Minimize(custo_var)
        
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        
        if status != cp_model.OPTIMAL:
            return None, []
        
        custo_otimo = int(solver.ObjectiveValue())
        model.Add(custo_var == custo_otimo)
        
        class SolutionCollector(cp_model.CpSolverSolutionCallback):
            def __init__(self, variables):
                cp_model.CpSolverSolutionCallback.__init__(self)
                self.variables = variables
                self.solutions = []
            def on_solution_callback(self):
                sol = {v for v in self.variables if self.Value(self.variables[v]) == 1}
                self.solutions.append(sol)
        
        collector = SolutionCollector(x)
        solver.SearchForAllSolutions(model, collector)
        
        print(f"\n✓ Todas as soluções ótimas:")
        print(f"  • Custo: {custo_otimo} guardas")
        print(f"  • Número de soluções: {len(collector.solutions)}")
        print(f"  • Soluções: {[sorted(s) for s in collector.solutions]}")
        
        return custo_otimo, collector.solutions


def main():
    solver = ORToolsSolver()
    
    # CP-SAT
    custo, sols = solver.resolver_cp_sat()
    
    # MIP (código original da professora)
    custo, sols = solver.resolver_mip()
    
    # Todas as soluções
    custo, todas = solver.resolver_todas_solucoes()


if __name__ == "__main__":
    main()