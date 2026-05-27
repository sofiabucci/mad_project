"""
ITEM 3 - Programação Dinâmica
Resolução por programação dinâmica 
Complexidade: O(2^n × m) onde n = número de retângulos, m = número de vértices
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.instancia import INSTANCIA
import time

class ProgramacaoDinamica:
    def __init__(self, instancia=None):
        self.instancia = instancia or INSTANCIA
        self.num_retangulos = self.instancia.num_retangulos
        
        # Máscara de bits para cada vértice
        self.vertice_mask = {}
        for v in self.instancia.vertices:
            mask = 0
            for rect in self.instancia.retangulos:
                if v in self.instancia.retangulos[rect]:
                    mask |= (1 << (rect - 1))
            self.vertice_mask[v] = mask
        
        self.meta = (1 << self.num_retangulos) - 1
    
    def resolver(self):
        """
        Programação Dinâmica com tabela:
        dp[mask] = (custo, conjunto_de_vértices)
        """
        print("\n" + "=" * 70)
        print("ITEM 3 - PROGRAMAÇÃO DINÂMICA")
        print("=" * 70)
        
        inicio = time.time()
        
        # Inicialização: dp[mask] = (custo, vertices)
        dp = {0: (0, set())}
        
        # Preencher DP para todas as máscaras
        for mask_atual in range(self.meta + 1):
            if mask_atual not in dp:
                continue
            
            custo_atual, vertices_atual = dp[mask_atual]
            
            for v in self.instancia.vertices:
                nova_mask = mask_atual | self.vertice_mask[v]
                novo_custo = custo_atual + 1
                
                if nova_mask not in dp:
                    dp[nova_mask] = (novo_custo, vertices_atual | {v})
                elif novo_custo < dp[nova_mask][0]:
                    dp[nova_mask] = (novo_custo, vertices_atual | {v})
        
        tempo = (time.time() - inicio) * 1000
        
        if self.meta in dp:
            custo, vertices = dp[self.meta]
            print(f"\n✓ Solução encontrada!")
            print(f"  • Tempo: {tempo:.3f} ms")
            print(f"  • Guardas: {sorted(vertices)}")
            print(f"  • Número: {custo}")
            
            # Análise de complexidade
            print("\n" + "-" * 50)
            print("ANÁLISE DE COMPLEXIDADE")
            print("-" * 50)
            print(f"  • Número de retângulos (n): {self.num_retangulos}")
            print(f"  • Número de vértices (m): {self.instancia.num_vertices}")
            print(f"  • Estados (2^n): {2**self.num_retangulos}")
            print(f"  • Operações: {2**self.num_retangulos * self.instancia.num_vertices}")
            print(f"  • Complexidade de espaço: O(2^n × m) = {2**self.num_retangulos * self.instancia.num_vertices} bytes aprox.")
            print(f"  • Complexidade de tempo: O(2^n × m)")
            
            return custo, vertices
        else:
            print("\n✗ Nenhuma solução encontrada")
            return None, None
    
    def resolver_memoizacao(self):
        """
        Versão com memoização recursiva
        """
        memo = {}
        
        def dp_rec(mask: int) -> tuple:
            if mask == self.meta:
                return (0, set())
            
            if mask in memo:
                return memo[mask]
            
            melhor_custo = float('inf')
            melhores_vertices = None
            
            for v in self.instancia.vertices:
                nova_mask = mask | self.vertice_mask[v]
                if nova_mask == mask:
                    continue  # Não adiciona novos retângulos
                
                custo, vertices = dp_rec(nova_mask)
                
                if custo + 1 < melhor_custo:
                    melhor_custo = custo + 1
                    melhores_vertices = vertices | {v}
            
            memo[mask] = (melhor_custo, melhores_vertices)
            return memo[mask]
        
        inicio = time.time()
        custo, vertices = dp_rec(0)
        tempo = (time.time() - inicio) * 1000
        
        print("\n" + "-" * 50)
        print("PROGRAMAÇÃO DINÂMICA COM MEMOIZAÇÃO")
        print("-" * 50)
        print(f"  • Tempo: {tempo:.3f} ms")
        print(f"  • Guardas: {sorted(vertices) if vertices else []}")
        print(f"  • Número: {custo if custo != float('inf') else 'N/A'}")
        
        return custo, vertices


def main():
    pd = ProgramacaoDinamica()
    custo, vertices = pd.resolver()
    
    if custo:
        # Verificar se é ótima
        custo_otimo = len(INSTANCIA.solucoes_optimas()[0])
        if custo == custo_otimo:
            print(f"\n✓ Solução ótima (custo = {custo_otimo})")
        else:
            print(f"\n✗ Solução subótima (ótimo = {custo_otimo})")
    
    # Versão com memoização
    pd.resolver_memoizacao()


if __name__ == "__main__":
    main()