"""
ITEM 4a - Extensão: Guardas com Cores
Guardas que veem o mesmo retângulo devem ter cores distintas

Problema: Minimizar número de guardas e depois minimizar número de cores
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.instancia import INSTANCIA

class ColoredGuards:
    def __init__(self, instancia=None):
        self.instancia = instancia or INSTANCIA
        self.vertice_para_rects = self.instancia.retangulos_por_vertice()
        
        # Calcular conflitos entre vértices (mesmo retângulo)
        self.conflitos = set()
        for rect, verts in self.instancia.retangulos.items():
            verts_lista = list(verts)
            for i in range(len(verts_lista)):
                for j in range(i + 1, len(verts_lista)):
                    self.conflitos.add((verts_lista[i], verts_lista[j]))
    
    def resolver_minimo_guardas(self):
        """Primeiro: encontrar número mínimo de guardas usando OR-Tools"""
        try:
            from ortools.sat.python import cp_model
        except ImportError:
            print("OR-Tools não instalado. Execute: pip install ortools")
            return None, None
        
        model = cp_model.CpModel()
        x = {v: model.NewBoolVar(f'x_{v}') for v in self.instancia.vertices}
        
        # Restrições de cobertura
        for rect, verts in self.instancia.retangulos.items():
            model.Add(sum(x[v] for v in verts) >= 1)
        
        model.Minimize(sum(x[v] for v in self.instancia.vertices))
        
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        
        if status == cp_model.OPTIMAL:
            min_guardas = int(solver.ObjectiveValue())
            guardas = {v for v in self.instancia.vertices if solver.Value(x[v]) == 1}
            return min_guardas, guardas
        return None, None
    
    def resolver_minimo_cores(self, guardas):
        """Segundo: encontrar número mínimo de cores para os guardas"""
        try:
            from ortools.sat.python import cp_model
        except ImportError:
            return None, None
        
        # Filtrar conflitos apenas entre guardas
        conflitos_guardas = [(u, v) for (u, v) in self.conflitos 
                            if u in guardas and v in guardas]
        
        if not conflitos_guardas:
            return 1, {v: 0 for v in guardas}
        
        model = cp_model.CpModel()
        max_cores = len(guardas)
        
        cores = {v: model.NewIntVar(0, max_cores - 1, f'cor_{v}') for v in guardas}
        
        for u, v in conflitos_guardas:
            model.Add(cores[u] != cores[v])
        
        cores_usadas = [model.NewBoolVar(f'c_{i}') for i in range(max_cores)]
        for v in guardas:
            for i in range(max_cores):
                model.Add(cores[v] == i).OnlyEnforceIf(cores_usadas[i])
                model.Add(cores[v] != i).OnlyEnforceIf(cores_usadas[i].Not())
        
        model.Minimize(sum(cores_usadas))
        
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        
        if status == cp_model.OPTIMAL:
            min_cores = int(solver.ObjectiveValue())
            cores_assign = {v: solver.Value(cores[v]) for v in guardas}
            return min_cores, cores_assign
        return None, None
    
    def resolver(self):
        """Resolve o problema completo"""
        print("\n" + "=" * 70)
        print("ITEM 4a - EXTENSÃO: GUARDAS COM CORES")
        print("=" * 70)
        
        print("\n1. Encontrando número mínimo de guardas...")
        min_guardas, guardas = self.resolver_minimo_guardas()
        
        if min_guardas is None:
            print("  ✗ Falha ao encontrar guardas")
            return
        
        print(f"  ✓ Mínimo de guardas: {min_guardas}")
        print(f"    Guardas: {sorted(guardas)}")
        
        print("\n2. Encontrando número mínimo de cores...")
        min_cores, cores = self.resolver_minimo_cores(guardas)
        
        if min_cores is None:
            print("  ✗ Falha ao encontrar cores")
            return
        
        print(f"  ✓ Mínimo de cores: {min_cores}")
        print("\n  Distribuição por cor:")
        for cor in range(min_cores):
            verts = [v for v in guardas if cores[v] == cor]
            print(f"    Cor {cor + 1}: {sorted(verts)}")
        
        print("\n" + "-" * 50)
        print("CONCLUSÃO")
        print("-" * 50)
        print(f"  • Número mínimo de guardas: {min_guardas}")
        print(f"  • Número mínimo de cores: {min_cores}")
        print(f"  • Guardas: {sorted(guardas)}")
        print(f"  • Cores: {cores}")


def main():
    solver = ColoredGuards()
    solver.resolver()

if __name__ == "__main__":
    main()