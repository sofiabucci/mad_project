# colored_guards.py
"""
Extensão: Guardas com cores - vértices que veem o mesmo retângulo devem ter cores diferentes
"""

from ortools.sat.python import cp_model
from typing import Set, Dict, List, Tuple
import time

class ColoredGuardsSolver:
    """
    Resolve o problema de guardas coloridos
    Guardas que cobrem o mesmo retângulo devem ter cores diferentes
    """
    
    def __init__(self, instancia):
        self.instancia = instancia
        self.retangulos = instancia.retangulos
        self.vertices = instancia.vertices
        self.num_vertices = len(self.vertices)
        self.num_retangulos = len(self.retangulos)
        
        # Mapeamento vértice -> retângulos
        self.vertice_para_rects = instancia.retangulos_por_vertice()
        
        # Matriz de conflitos: dois vértices conflitam se cobrem o mesmo retângulo
        self.conflitos = self._calcular_conflitos()
    
    def _calcular_conflitos(self) -> Set[Tuple[int, int]]:
        """Calcula pares de vértices que conflitam (veem o mesmo retângulo)"""
        conflitos = set()
        
        for rect, verts in self.retangulos.items():
            verts_lista = list(verts)
            for i in range(len(verts_lista)):
                for j in range(i + 1, len(verts_lista)):
                    conflitos.add((verts_lista[i], verts_lista[j]))
        
        return conflitos
    
    def resolver_minimo_guardas(self) -> Tuple[int, Set[int], int]:
        """
        Passo 1: Encontrar número mínimo de guardas
        """
        print("\n" + "=" * 80)
        print("EXTENSÃO 1: GUARDAS COM CORES")
        print("=" * 80)
        
        print("\n1. ENCONTRANDO MÍNIMO DE GUARDAS")
        print("-" * 50)
        
        model = cp_model.CpModel()
        
        # Variáveis de guarda
        x = {v: model.NewBoolVar(f'x_{v}') for v in self.vertices}
        
        # Restrições de cobertura
        for rect, verts in self.retangulos.items():
            model.Add(sum(x[v] for v in verts) >= 1)
        
        # Objetivo
        model.Minimize(sum(x[v] for v in self.vertices))
        
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        
        if status == cp_model.OPTIMAL:
            min_guardas = int(solver.ObjectiveValue())
            guardas = {v for v in self.vertices if solver.Value(x[v]) == 1}
            print(f"✓ Mínimo de guardas: {min_guardas}")
            print(f"  Guardas: {sorted(guardas)}")
            return min_guardas, guardas, None
        else:
            print("✗ Não foi possível encontrar solução")
            return None, None, None
    
    def resolver_minimo_cores(self, guardas: Set[int]) -> Tuple[int, Dict[int, int]]:
        """
        Passo 2: Encontrar número mínimo de cores para os guardas
        Problema de coloração de vértices no subgrafo induzido pelos guardas
        """
        print("\n2. ENCONTRANDO MÍNIMO DE CORES")
        print("-" * 50)
        
        # Filtrar conflitos apenas entre guardas
        conflitos_guardas = [(u, v) for (u, v) in self.conflitos 
                            if u in guardas and v in guardas]
        
        if not conflitos_guardas:
            print("✓ Sem conflitos entre guardas -> 1 cor suficiente")
            return 1, {v: 0 for v in guardas}
        
        model = cp_model.CpModel()
        
        # Número máximo de cores possível = número de guardas
        max_cores = len(guardas)
        
        # Variáveis de cor
        cores = {v: model.NewIntVar(0, max_cores - 1, f'cor_{v}') for v in guardas}
        
        # Restrições de conflito
        for u, v in conflitos_guardas:
            model.Add(cores[u] != cores[v])
        
        # Minimizar número de cores (usando variável auxiliar)
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
            print(f"✓ Número mínimo de cores: {min_cores}")
            
            # Mostrar distribuição por cor
            print("\n  Distribuição por cor:")
            for cor in range(min_cores):
                verts = [v for v in guardas if cores_assign[v] == cor]
                if verts:
                    print(f"    Cor {cor + 1}: {sorted(verts)}")
            
            return min_cores, cores_assign
        else:
            print("✗ Não foi possível encontrar solução de coloração")
            return None, None
    
    def resolver_conjunto(self) -> Tuple[int, int, Set[int], Dict[int, int]]:
        """Resolve o problema completo: minimizar guardas e depois cores"""
        
        # Passo 1: Encontrar guardas
        min_guardas, guardas, _ = self.resolver_minimo_guardas()
        if min_guardas is None:
            return None, None, None, None
        
        # Passo 2: Encontrar cores para esses guardas
        min_cores, cores_assign = self.resolver_minimo_cores(guardas)
        
        print("\n" + "=" * 80)
        print("RESULTADO FINAL")
        print("=" * 80)
        print(f"\n• Número mínimo de guardas: {min_guardas}")
        print(f"• Número mínimo de cores: {min_cores}")
        print(f"• Guardas: {sorted(guardas)}")
        
        return min_guardas, min_cores, guardas, cores_assign

# ============================================================
# EXTENSÃO 2: GUARDAS COM MAIOR ALCANCE
# ============================================================

class GuardasAlcance:
    """
    Extensão: Guardas podem cobrir retângulos a uma distância D no grafo
    """
    
    def __init__(self, instancia, distancia: int = 1):
        self.instancia = instancia
        self.distancia = distancia
        self.vertices = instancia.vertices
        self.retangulos = instancia.retangulos
        
        # Grafo de adjacência entre vértices (baseado em compartilhar retângulos)
        self.grafo = self._construir_grafo()
        
        # Calcular alcance de cada vértice
        self.alcance = self._calcular_alcance()
    
    def _construir_grafo(self) -> Dict[int, Set[int]]:
        """Constrói grafo onde arestas conectam vértices que cobrem o mesmo retângulo"""
        grafo = {v: set() for v in self.vertices}
        
        for rect, verts in self.retangulos.items():
            verts_lista = list(verts)
            for i in range(len(verts_lista)):
                for j in range(i + 1, len(verts_lista)):
                    u, w = verts_lista[i], verts_lista[j]
                    grafo[u].add(w)
                    grafo[w].add(u)
        
        return grafo
    
    def _calcular_alcance(self) -> Dict[int, Set[int]]:
        """
        Calcula o conjunto de retângulos que cada vértice pode cobrir
        a uma distância até D no grafo
        """
        alcance = {}
        
        for v in self.vertices:
            # BFS para encontrar vértices a distância ≤ D
            visitados = {v}
            fila = [(v, 0)]
            vertices_alcance = {v}
            
            while fila:
                atual, dist = fila.pop(0)
                if dist >= self.distancia:
                    continue
                for vizinho in self.grafo[atual]:
                    if vizinho not in visitados:
                        visitados.add(vizinho)
                        vertices_alcance.add(vizinho)
                        fila.append((vizinho, dist + 1))
            
            # Retângulos cobertos por esses vértices
            rects = set()
            for vert in vertices_alcance:
                for rect, verts in self.retangulos.items():
                    if vert in verts:
                        rects.add(rect)
            
            alcance[v] = rects
        
        return alcance
    
    def resolver(self) -> Tuple[int, Set[int]]:
        """Resolve o problema com guardas de maior alcance"""
        print("\n" + "=" * 80)
        print(f"EXTENSÃO 2: GUARDAS COM ALCANCE D = {self.distancia}")
        print("=" * 80)
        
        print(f"\nAlcance de cada vértice:")
        for v in self.vertices:
            print(f"  Vértice {v}: {len(self.alcance[v])} retângulos")
        
        model = cp_model.CpModel()
        
        # Variáveis de guarda
        x = {v: model.NewBoolVar(f'x_{v}') for v in self.vertices}
        
        # Restrições: cada retângulo deve ser coberto por algum vértice no alcance
        for rect in self.retangulos:
            # Vértices que podem cobrir este retângulo
            cobrem = [v for v in self.vertices if rect in self.alcance[v]]
            model.Add(sum(x[v] for v in cobrem) >= 1)
        
        # Objetivo
        model.Minimize(sum(x[v] for v in self.vertices))
        
        solver = cp_model.CpSolver()
        inicio = time.time()
        status = solver.Solve(model)
        tempo = time.time() - inicio
        
        if status == cp_model.OPTIMAL:
            custo = int(solver.ObjectiveValue())
            guardas = {v for v in self.vertices if solver.Value(x[v]) == 1}
            print(f"\n✓ Solução encontrada em {tempo:.4f} segundos")
            print(f"  Guardas: {sorted(guardas)}")
            print(f"  Número: {custo}")
            
            # Mostrar cobertura
            print("\n  Cobertura detalhada:")
            for rect in sorted(self.retangulos.keys()):
                guardas_cobrem = [v for v in guardas if rect in self.alcance[v]]
                print(f"    Retângulo {rect}: coberto por {guardas_cobrem}")
            
            return custo, guardas
        else:
            print("✗ Nenhuma solução encontrada")
            return None, None

def main_extensoes():
    """Executa as extensões do problema"""
    
    from rect_coverage_solver import InstanciaParticao
    
    instancia = InstanciaParticao()
    
    print("\n" + "=" * 80)
    print("EXTENSÕES DO PROBLEMA")
    print("=" * 80)
    
    # Extensão 1: Guardas coloridos
    solver_cores = ColoredGuardsSolver(instancia)
    min_guardas, min_cores, guardas, cores = solver_cores.resolver_conjunto()
    
    # Extensão 2: Guardas com alcance
    print("\n" + "-" * 80)
    for D in [1, 2]:
        solver_alcance = GuardasAlcance(instancia, distancia=D)
        custo, guardas = solver_alcance.resolver()

if __name__ == "__main__":
    main_extensoes()