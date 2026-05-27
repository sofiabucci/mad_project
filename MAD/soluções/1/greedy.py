"""
ITEM 1 - Estratégias Greedy
Avaliação de diferentes estratégias greedy para colocação de guardas

Estratégias implementadas:
- E1: First-Fail (retângulo com menos vértices incidentes)
- E2: Max Coverage (vértice que cobre mais retângulos)
- E3: Vértices Raros (vértices que aparecem em menos retângulos)
- E4: Hierárquica (obrigatórios primeiro, depois greedy)

Relação com First-Fail em CSPs:
O retângulo com menos vértices incidentes corresponde à variável com
menor domínio num CSP. Escolhê-lo primeiro aplica o princípio de
"falhar cedo" (fail early), reduzindo o espaço de busca.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from instancia import INSTANCIA
import time

class EstrategiaGreedy:
    def __init__(self, instancia=None):
        self.instancia = instancia or INSTANCIA
        self.vertice_para_rects = self.instancia.retangulos_por_vertice()
    
    # ----------------------------------------------------------
    # E1: First-Fail (retângulo com menos vértices)
    # ----------------------------------------------------------
    def first_fail(self):
        """
        First-Fail: escolhe o retângulo com MENOS vértices incidentes
        (equivalente a escolher a variável com menor domínio num CSP)
        """
        guardas = set()
        cobertos = set()
        
        # Ordenar retângulos por número de vértices (crescente)
        retangulos_ordenados = sorted(
            self.instancia.retangulos.items(),
            key=lambda x: len(x[1])
        )
        
        while len(cobertos) < self.instancia.num_retangulos:
            # Encontrar primeiro retângulo não coberto
            alvo = None
            for rect, verts in retangulos_ordenados:
                if rect not in cobertos:
                    alvo = (rect, verts)
                    break
            
            if alvo is None:
                break
            
            rect_alvo, verts_alvo = alvo
            
            # No retângulo crítico, escolher vértice que cobre mais
            melhor_v = None
            melhor_contagem = -1
            
            for v in verts_alvo:
                novos = len(self.vertice_para_rects[v] - cobertos)
                if novos > melhor_contagem:
                    melhor_contagem = novos
                    melhor_v = v
            
            if melhor_v:
                guardas.add(melhor_v)
                cobertos.update(self.vertice_para_rects[melhor_v])
        
        return guardas
    
    # ----------------------------------------------------------
    # E2: Max Coverage (vértice que cobre mais)
    # ----------------------------------------------------------
    def max_coverage(self):
        """
        Greedy padrão: escolher vértice que cobre mais retângulos não cobertos
        """
        guardas = set()
        cobertos = set()
        
        while len(cobertos) < self.instancia.num_retangulos:
            melhor_v = None
            melhor_contagem = -1
            
            for v in self.instancia.vertices:
                if v in guardas:
                    continue
                novos = len(self.vertice_para_rects[v] - cobertos)
                if novos > melhor_contagem:
                    melhor_contagem = novos
                    melhor_v = v
            
            if melhor_v:
                guardas.add(melhor_v)
                cobertos.update(self.vertice_para_rects[melhor_v])
            else:
                break
        
        return guardas
    
    # ----------------------------------------------------------
    # E3: Vértices Raros (menos frequentes)
    # ----------------------------------------------------------
    def vertices_raros(self):
        """
        Priorizar vértices que aparecem em poucos retângulos
        """
        guardas = set()
        cobertos = set()
        
        # Ordenar vértices por frequência (crescente = mais raros)
        vertices_ordenados = sorted(
            self.instancia.vertices,
            key=lambda v: len(self.vertice_para_rects[v])
        )
        
        for v in vertices_ordenados:
            if len(self.vertice_para_rects[v] - cobertos) > 0:
                guardas.add(v)
                cobertos.update(self.vertice_para_rects[v])
        
        return guardas
    
    # ----------------------------------------------------------
    # E4: Hierárquica (obrigatórios + greedy)
    # ----------------------------------------------------------
    def hierarquica(self):
        """
        Hierárquica:
        1. Vértices obrigatórios (retângulos com apenas 1 vértice)
        2. Greedy max coverage para o restante
        """
        guardas = set()
        cobertos = set()
        
        # Passo 1: vértices obrigatórios
        for rect, verts in self.instancia.retangulos.items():
            if len(verts) == 1:
                v = next(iter(verts))
                if v not in guardas:
                    guardas.add(v)
                    cobertos.update(self.vertice_para_rects[v])
        
        # Passo 2: greedy para o restante
        while len(cobertos) < self.instancia.num_retangulos:
            melhor_v = None
            melhor_contagem = -1
            
            for v in self.instancia.vertices:
                if v in guardas:
                    continue
                novos = len(self.vertice_para_rects[v] - cobertos)
                if novos > melhor_contagem:
                    melhor_contagem = novos
                    melhor_v = v
            
            if melhor_v:
                guardas.add(melhor_v)
                cobertos.update(self.vertice_para_rects[melhor_v])
            else:
                break
        
        return guardas


def main():
    print("=" * 70)
    print("ITEM 1 - AVALIAÇÃO DE ESTRATÉGIAS GREEDY")
    print("=" * 70)
    
    print(INSTANCIA)
    
    estrategias = {
        "E1 - First-Fail (retângulo menos opções)": EstrategiaGreedy.first_fail,
        "E2 - Max Coverage (vértice mais retângulos)": EstrategiaGreedy.max_coverage,
        "E3 - Vértices Raros": EstrategiaGreedy.vertices_raros,
        "E4 - Hierárquica (obrigatórios + greedy)": EstrategiaGreedy.hierarquica
    }
    
    print("\n" + "-" * 70)
    print(f"{'Estratégia':<40} {'Guardas':<10} {'Tempo(ms)':<12} {'Solução'}")
    print("-" * 70)
    
    resultados = {}
    
    for nome, estrategia in estrategias.items():
        greedy = EstrategiaGreedy()
        inicio = time.time()
        solucao = estrategia(greedy)
        tempo = (time.time() - inicio) * 1000
        
        resultados[nome] = {
            'solucao': solucao,
            'tamanho': len(solucao),
            'tempo': tempo,
            'valida': INSTANCIA.verificar_solucao(solucao)
        }
        
        valida_str = "✓" if resultados[nome]['valida'] else "✗"
        print(f"{nome:<40} {len(solucao):<10} {tempo:<12.3f} {sorted(solucao)} {valida_str}")
    
    # Análise da relação com First-Fail
    print("\n" + "=" * 70)
    print("RELAÇÃO COM FIRST-FAIL (CSPs)")
    print("=" * 70)
    print("""
    ┌─────────────────────────────────────────────────────────────────────┐
    │                    RELAÇÃO FIRST-FAIL                               │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │   FIRST-FAIL em CSPs          ↔    ESTRATÉGIA E1                    │
    │                                                                     │
    │   • Variável c/ menor domínio  ↔    Retângulo c/ menos vértices     │
    │   • Falhar cedo (fail early)   ↔    Decisão crítica primeiro        │
    │   • Reduz espaço de busca      ↔    Evita backtracking excessivo    │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
    
    Justificativa: O retângulo com menos vértices incidentes é o mais 
    restritivo. Se não for coberto cedo, pode forçar backtracking. 
    Esta é a aplicação direta do princípio first-fail.
    """)
    
    # Comparação com ótimo
    print("=" * 70)
    print("COMPARAÇÃO COM SOLUÇÃO ÓTIMA")
    print("=" * 70)
    
    sol_otima = INSTANCIA.solucoes_optimas()
    custo_otimo = len(sol_otima[0])
    
    print(f"\nSoluções ótimas conhecidas: {sol_otima}")
    print(f"Custo ótimo: {custo_otimo} guardas\n")
    
    for nome, dados in resultados.items():
        if dados['tamanho'] == custo_otimo:
            print(f"  ✓ {nome}: ÓTIMA")
        else:
            print(f"  ✗ {nome}: SUBÓTIMA ({dados['tamanho'] - custo_otimo} acima)")
    
    print("\n" + "=" * 70)
    print("CONCLUSÃO")
    print("=" * 70)
    print("""
    A melhor estratégia greedy para esta instância é a E4 (Hierárquica),
    seguida pela E1 (First-Fail) e E2 (Max Coverage). A estratégia E3
    (Vértices Raros) não garante otimalidade.
    
    Recomendação: Para problemas pequenos, usar E4; para problemas grandes,
    usar E1 (First-Fail) pois reduz o espaço de busca.
    """)


if __name__ == "__main__":
    main()