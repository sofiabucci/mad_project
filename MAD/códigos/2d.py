# ortools_solver.py
"""
Resolução do problema com Google OR-Tools
"""

from ortools.sat.python import cp_model
from typing import List, Set, Tuple
import time

class GuardasSolver:
    """Solver usando CP-SAT do OR-Tools"""
    
    def __init__(self):
        self.vertices = list(range(1, 9))
        self.retangulos = {
            1: [1], 2: [1, 2], 3: [3, 4], 4: [2, 3, 4, 5],
            5: [5, 6], 6: [6, 7], 7: [6, 7, 8], 8: [7, 8],
            9: [1, 2, 3, 4, 5], 10: [8]
        }
        self.num_vertices = 8
        self.num_retangulos = 10
    
    def resolver_cp_sat(self) -> Tuple[int, List[Set[int]]]:
        """Resolve usando CP-SAT"""
        print("\n" + "=" * 80)
        print("RESOLUÇÃO COM OR-TOOLS (CP-SAT)")
        print("=" * 80)
        
        inicio = time.time()
        
        model = cp_model.CpModel()
        
        # Variáveis
        x = {v: model.NewBoolVar(f'x_{v}') for v in self.vertices}
        
        # Restrições
        for rect, verts in self.retangulos.items():
            model.Add(sum(x[v] for v in verts) >= 1)
        
        # Objetivo
        model.Minimize(sum(x[v] for v in self.vertices))
        
        # Resolver
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10.0
        
        status = solver.Solve(model)
        tempo = time.time() - inicio
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            custo = int(solver.ObjectiveValue())
            solucao = {v for v in self.vertices if solver.Value(x[v]) == 1}
            print(f"Status: {'ÓTIMO' if status == cp_model.OPTIMAL else 'VIÁVEL'}")
            print(f"Tempo: {tempo:.4f} segundos")
            print(f"Guardas: {sorted(solucao)}")
            print(f"Número: {custo}")
            return custo, [solucao]
        else:
            print("Nenhuma solução encontrada")
            return None, []
    
    def resolver_mip(self) -> Tuple[int, List[Set[int]]]:
        """Resolve usando MIP (Mixed Integer Programming)"""
        print("\n" + "=" * 80)
        print("RESOLUÇÃO COM OR-TOOLS (MIP)")
        print("=" * 80)
        
        try:
            from ortools.linear_solver import pywraplp
        except ImportError:
            print("MIP não disponível")
            return None, []
        
        inicio = time.time()
        
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            print("Solver SCIP não disponível")
            return None, []
        
        # Variáveis
        x = {v: solver.IntVar(0, 1, f'x_{v}') for v in self.vertices}
        
        # Restrições
        for rect, verts in self.retangulos.items():
            solver.Add(sum(x[v] for v in verts) >= 1)
        
        # Objetivo
        objective = solver.Objective()
        for v in self.vertices:
            objective.SetCoefficient(x[v], 1)
        objective.SetMinimization()
        
        # Resolver
        status = solver.Solve()
        tempo = time.time() - inicio
        
        if status == pywraplp.Solver.OPTIMAL:
            custo = int(objective.Value())
            solucao = {v for v in self.vertices if x[v].solution_value() > 0.5}
            print(f"Tempo: {tempo:.4f} segundos")
            print(f"Guardas: {sorted(solucao)}")
            print(f"Número: {custo}")
            return custo, [solucao]
        else:
            print("Nenhuma solução ótima encontrada")
            return None, []
    
    def resolver_todas_solucoes(self) -> Tuple[int, List[Set[int]]]:
        """Encontra todas as soluções ótimas usando CP-SAT"""
        print("\n" + "=" * 80)
        print("TODAS AS SOLUÇÕES ÓTIMAS (OR-TOOLS)")
        print("=" * 80)
        
        inicio = time.time()
        
        model = cp_model.CpModel()
        
        # Variáveis
        x = {v: model.NewBoolVar(f'x_{v}') for v in self.vertices}
        
        # Restrições
        for rect, verts in self.retangulos.items():
            model.Add(sum(x[v] for v in verts) >= 1)
        
        # Objetivo
        custo_var = model.NewIntVar(0, self.num_vertices, 'custo')
        model.Add(custo_var == sum(x[v] for v in self.vertices))
        model.Minimize(custo_var)
        
        # Resolver uma vez para encontrar o custo ótimo
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        
        if status != cp_model.OPTIMAL:
            print("Não foi possível encontrar solução ótima")
            return None, []
        
        custo_otimo = int(solver.ObjectiveValue())
        
        # Adicionar restrição para fixar o custo
        model.Add(custo_var == custo_otimo)
        
        # Coletar todas as soluções
        class SolucaoCollector(cp_model.CpSolverSolutionCallback):
            def __init__(self, variables):
                cp_model.CpSolverSolutionCallback.__init__(self)
                self.variables = variables
                self.solucoes = []
            
            def on_solution_callback(self):
                sol = {v for v in self.variables if self.Value(self.variables[v]) == 1}
                self.solucoes.append(sol)
        
        collector = SolucaoCollector(x)
        solver.SearchForAllSolutions(model, collector)
        
        tempo = time.time() - inicio
        
        print(f"Custo ótimo: {custo_otimo}")
        print(f"Número de soluções: {len(collector.solucoes)}")
        print(f"Tempo: {tempo:.4f} segundos")
        
        return custo_otimo, collector.solucoes

def comparar_metodos():
    """Compara os diferentes métodos de resolução"""
    
    solver = GuardasSolver()
    
    print("\n" + "=" * 80)
    print("COMPARAÇÃO DE MÉTODOS DE RESOLUÇÃO")
    print("=" * 80)
    
    resultados = {}
    
    # CP-SAT
    custo, sols = solver.resolver_cp_sat()
    if custo:
        resultados["CP-SAT"] = (custo, len(sols))
    
    # MIP
    custo, sols = solver.resolver_mip()
    if custo:
        resultados["MIP (SCIP)"] = (custo, len(sols))
    
    # Todas as soluções
    custo, sols = solver.resolver_todas_solucoes()
    if custo:
        resultados["Todas Soluções"] = (custo, len(sols))
    
    print("\n" + "-" * 50)
    print("RESUMO:")
    print("-" * 50)
    for metodo, (custo, n_sols) in resultados.items():
        print(f"  {metodo}: {custo} guardas, {n_sols} solução(ões)")

if __name__ == "__main__":
    comparar_metodos()