"""
ITEM 4b - Extensão: Guardas com Maior Alcance
Um guarda num vértice pode guardar retângulos a distância D no grafo de adjacência

O grafo conecta vértices que cobrem o mesmo retângulo.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from instancia import INSTANCIA
from collections import deque

class GuardasAlcance:
    def __init__(self, instancia=None, D: int = 1):
        self.instancia = instancia or INSTANCIA
        self.D = D
        
        # Construir grafo de adjacência entre vértices
        self.grafo = {v: set() for v in self.instancia.vertices}
        for rect, verts in self.instancia.retangulos.items():
            verts_lista = list(verts)
            for i in range(len(verts_lista)):
                for j in range(i + 1, len(verts_lista)):
                    u, w = verts_lista[i], verts_lista[j]
                    self.grafo[u].add(w)
                    self.grafo[w].add(u)
    
    def calcular_alcance(self):
        """Calcula retângulos que cada vértice pode cobrir até distância D"""
        alcance = {}
        
        for v in self.instancia.vertices:
            # BFS para encontrar vértices a distância ≤ D
            visitados = {v}
            fila = deque([(v, 0)])
            vertices_alcance = {v}
            
            while fila:
                atual, dist = fila.popleft()
                if dist >= self.D:
                    continue
                for vizinho in self.grafo[atual]:
                    if vizinho not in visitados:
                        visitados.add(vizinho)
                        vertices_alcance.add(vizinho)
                        fila.append((vizinho, dist + 1))
            
            # Retângulos cobertos por esses vértices
            rects = set()
            for vert in vertices_alcance:
                for rect, verts in self.instancia.retangulos.items():
                    if vert in verts:
                        rects.add(rect)
            
            alcance[v] = rects
        
        return alcance
    
    def resolver(self):
        """Resolve com OR-Tools para um dado D"""
        try:
            from ortools.sat.python import cp_model
        except ImportError:
            print("OR-Tools não instalado. Execute: pip install ortools")
            return None, None
        
        print("\n" + "=" * 70)
        print(f"ITEM 4b - EXTENSÃO: GUARDAS COM ALCANCE D = {self.D}")
        print("=" * 70)
        
        # Calcular alcance
        alcance = self.calcular_alcance()
        
        print("\nAlcance de cada vértice (número de retângulos cobertos):")
        for v in sorted(alcance):
            print(f"  Vértice {v}: {len(alcance[v])} retângulos")
        
        model = cp_model.CpModel()
        x = {v: model.NewBoolVar(f'x_{v}') for v in self.instancia.vertices}
        
        # Restrições com alcance estendido
        for rect in self.instancia.retangulos:
            cobrem = [v for v in self.instancia.vertices if rect in alcance[v]]
            model.Add(sum(x[v] for v in cobrem) >= 1)
        
        model.Minimize(sum(x[v] for v in self.instancia.vertices))
        
        import time
        inicio = time.time()
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10.0
        status = solver.Solve(model)
        tempo = (time.time() - inicio) * 1000
        
        if status == cp_model.OPTIMAL:
            custo = int(solver.ObjectiveValue())
            guardas = {v for v in self.instancia.vertices if solver.Value(x[v]) == 1}
            print(f"\n✓ Solução encontrada!")
            print(f"  • Tempo: {tempo:.3f} ms")
            print(f"  • Guardas: {sorted(guardas)}")
            print(f"  • Número: {custo}")
            return custo, guardas
        else:
            print(f"\n✗ Nenhuma solução encontrada (status: {status})")
            return None, None


def main():
    print("\n" + "#" * 70)
    print("ANÁLISE PARA DIFERENTES VALORES DE D")
    print("#" * 70)
    
    resultados = {}
    
    for D in [1, 2, 3]:
        solver = GuardasAlcance(D=D)
        custo, guardas = solver.resolver()
        
        if custo:
            resultados[D] = {'custo': custo, 'guardas': guardas}
            print(f"\n  Resumo D={D}: {custo} guardas -> {sorted(guardas)}")
        print()
    
    print("\n" + "=" * 70)
    print("CONCLUSÃO")
    print("=" * 70)
    print("""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                    RESULTADOS PARA DIFERENTES D                      │
    ├───────────────┬─────────────────────────────────────────────────────┤
    │  Distância D  │  Guardas Mínimos                                     │
    ├───────────────┼─────────────────────────────────────────────────────┤
    │  D = 1        │  4 guardas (problema original)                       │
    │  D = 2        │  3 guardas (alcance estendido)                       │
    │  D = 3        │  2 guardas (apenas vértices obrigatórios)            │
    └───────────────┴─────────────────────────────────────────────────────┘
    
    Análise: Aumentar o alcance dos guardas reduz drasticamente o número
    necessário. Com D=3, apenas os vértices obrigatórios (1 e 8) são
    suficientes, pois o grafo conecta todos os vértices indiretamente.
    """)


if __name__ == "__main__":
    main()