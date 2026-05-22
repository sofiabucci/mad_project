# dynamic_programming.py
"""
Resolução do problema usando Programação Dinâmica
"""

from typing import Set, Dict, List, Tuple
from itertools import combinations
import time

class ProgramacaoDinamica:
    """
    Resolve o problema de cobertura usando programação dinâmica
    Estados: subconjuntos de retângulos cobertos
    """
    
    def __init__(self, instancia):
        self.instancia = instancia
        self.retangulos = instancia.retangulos
        self.vertices = instancia.vertices
        self.num_retangulos = len(self.retangulos)
        self.num_vertices = len(self.vertices)
        
        # Mapeamento vértice -> retângulos cobertos (bitmask)
        self.vertice_mask = {}
        for v in self.vertices:
            mask = 0
            for rect in self.retangulos:
                if v in self.retangulos[rect]:
                    mask |= (1 << (rect - 1))
            self.vertice_mask[v] = mask
        
        # Estado completo: todos os retângulos cobertos
        self.meta = (1 << self.num_retangulos) - 1
    
    def resolver_pd(self) -> Tuple[int, List[Set[int]]]:
        """
        Resolve por programação dinâmica
        dp[mask] = melhor custo para cobrir máscara de retângulos
        """
        print("\n" + "=" * 80)
        print("RESOLUÇÃO POR PROGRAMAÇÃO DINÂMICA")
        print("=" * 80)
        
        inicio = time.time()
        
        # Inicialização
        dp = {0: (0, set())}  # mask -> (custo, {vértices usados})
        
        # Ordenar máscaras por número de bits (heurística)
        mascaras = list(range(1, self.meta + 1))
        mascaras.sort(key=lambda x: bin(x).count('1'))
        
        for mask in mascaras:
            dp[mask] = (float('inf'), None)
        
        # Preencher DP
        for mask_atual in range(self.meta + 1):
            if mask_atual not in dp:
                continue
            
            custo_atual, vertices_atual = dp[mask_atual]
            
            for v in self.vertices:
                nova_mask = mask_atual | self.vertice_mask[v]
                novo_custo = custo_atual + 1
                
                if nova_mask not in dp:
                    dp[nova_mask] = (novo_custo, vertices_atual | {v})
                elif novo_custo < dp[nova_mask][0]:
                    dp[nova_mask] = (novo_custo, vertices_atual | {v})
        
        tempo = time.time() - inicio
        
        if self.meta in dp:
            custo, vertices_usados = dp[self.meta]
            print(f"Tempo de execução: {tempo:.4f} segundos")
            print(f"Guardas: {sorted(vertices_usados)}")
            print(f"Número: {custo}")
            return custo, [vertices_usados]
        else:
            print(f"Nenhuma solução encontrada")
            return None, []
    
    def resolver_pd_memo(self) -> Tuple[int, Set[int]]:
        """
        Resolve por programação dinâmica com memoização (recursiva)
        """
        memo = {}
        
        def dp_recursivo(mask: int) -> Tuple[int, Set[int]]:
            if mask == self.meta:
                return 0, set()
            
            if mask in memo:
                return memo[mask]
            
            melhor_custo = float('inf')
            melhor_vertices = None
            
            for v in self.vertices:
                if (mask & self.vertice_mask[v]) == self.vertice_mask[v]:
                    continue  # Não adiciona novos retângulos
                
                nova_mask = mask | self.vertice_mask[v]
                custo, vertices = dp_recursivo(nova_mask)
                
                if custo + 1 < melhor_custo:
                    melhor_custo = custo + 1
                    melhor_vertices = vertices | {v}
            
            memo[mask] = (melhor_custo, melhor_vertices)
            return memo[mask]
        
        inicio = time.time()
        custo, vertices = dp_recursivo(0)
        tempo = time.time() - inicio
        
        print("\n" + "=" * 80)
        print("PROGRAMAÇÃO DINÂMICA COM MEMOIZAÇÃO")
        print("=" * 80)
        print(f"Tempo de execução: {tempo:.4f} segundos")
        print(f"Guardas: {sorted(vertices)}")
        print(f"Número: {custo}")
        
        return custo, vertices
    
    def analisar_complexidade(self):
        """Analisa a complexidade do algoritmo"""
        print("\n" + "=" * 80)
        print("ANÁLISE DE COMPLEXIDADE")
        print("=" * 80)
        
        n_rect = self.num_retangulos
        n_vert = self.num_vertices
        
        print(f"""
Número de retângulos: {n_rect}
Número de vértices: {n_vert}

COMPLEXIDADE DE ESPAÇO:
  dp armazena 2^{n_rect} = {2**n_rect} estados
  Cada estado armazena:
    - custo (inteiro)
    - conjunto de vértices (até {n_vert} elementos)
  Espaço total: O(2^{n_rect} * {n_vert})

COMPLEXIDADE DE TEMPO:
  Para cada estado (2^{n_rect} = {2**n_rect})
  Para cada vértice ({n_vert})
  Operações O(1)
  Tempo total: O({2**n_rect} * {n_vert}) = {2**n_rect * n_vert} operações

MELHORIA POSSÍVEL:
  Para n_rect = {n_rect}, o problema é pequeno.
  Para n_rect > 20, a PD torna-se inviável.
  
  Neste caso, n_rect = {n_rect} < 20, a PD é viável.
""")

def comparar_abordagens():
    """Compara as diferentes abordagens de programação dinâmica"""
    
    from rect_coverage_solver import InstanciaParticao
    
    instancia = InstanciaParticao()
    pd = ProgramacaoDinamica(instancia)
    
    # Análise de complexidade
    pd.analisar_complexidade()
    
    # PD com tabela
    custo1, sols1 = pd.resolver_pd()
    
    # PD com memoização
    custo2, sols2 = pd.resolver_pd_memo()
    
    print("\n" + "=" * 80)
    print("COMPARAÇÃO DAS ABORDAGENS")
    print("=" * 80)
    
    if custo1 == custo2:
        print(f"\n✓ Ambas as abordagens encontraram a mesma solução ótima: {custo1} guardas")
    else:
        print(f"\n✗ Abordagens encontraram resultados diferentes: {custo1} vs {custo2}")

if __name__ == "__main__":
    comparar_abordagens()