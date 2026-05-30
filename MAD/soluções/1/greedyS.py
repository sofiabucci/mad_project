import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from instancia import INSTANCIA

class EstrategiaGreedy:
    def __init__(self, instancia):
        self.instancia = instancia
        self.vertice_para_rects = self.instancia.retangulos_por_vertice()
    
    def first_fail(self):
        """Estratégia First-Fail: escolher retângulo com menos vértices primeiro"""
        guardas, cobertos = set(), set()
        retangulos_ordenados = sorted(self.instancia.retangulos.items(), key=lambda x: len(x[1]))
        
        while len(cobertos) < self.instancia.num_retangulos:
            # Encontrar próximo retângulo não coberto
            alvo = next((r for r in retangulos_ordenados if r[0] not in cobertos), None)
            if not alvo: 
                break
            _, verts_alvo = alvo
            
            # Escolher vértice que cobre mais retângulos novos
            melhor_v = max(verts_alvo, key=lambda v: len(self.vertice_para_rects[v] - cobertos), default=None)
            if melhor_v:
                guardas.add(melhor_v)
                cobertos.update(self.vertice_para_rects[melhor_v])
        return guardas
    
    def max_coverage(self):
        """Estratégia Max Coverage: escolher vértice que cobre mais retângulos"""
        guardas, cobertos = set(), set()
        
        while len(cobertos) < self.instancia.num_retangulos:
            melhor_v, melhor_contagem = None, -1
            for v in self.instancia.vertices:
                if v in guardas:
                    continue
                novos = len(self.vertice_para_rects[v] - cobertos)
                if novos > melhor_contagem:
                    melhor_contagem = novos
                    melhor_v = v
                    
            if melhor_v and melhor_contagem > 0:
                guardas.add(melhor_v)
                cobertos.update(self.vertice_para_rects[melhor_v])
            else:
                break
        return guardas

    def vertices_raros(self):
        """Estratégia Vértices Raros: escolher vértices que aparecem em menos retângulos"""
        guardas, cobertos = set(), set()
        vertices_ordenados = sorted(self.instancia.vertices, key=lambda v: len(self.vertice_para_rects[v]))
        
        for v in vertices_ordenados:
            if len(self.vertice_para_rects[v] - cobertos) > 0:
                guardas.add(v)
                cobertos.update(self.vertice_para_rects[v])
        return guardas

    def hierarquica(self):
        """Estratégia Hierárquica: primeiro vértices obrigatórios, depois greedy"""
        guardas, cobertos = set(), set()
        
        # Passo 1: Colocar guardas em retângulos com apenas 1 vértice (obrigatórios)
        for rect, verts in self.instancia.retangulos.items():
            if len(verts) == 1:
                v = next(iter(verts))
                if v not in guardas:
                    guardas.add(v)
                    cobertos.update(self.vertice_para_rects[v])
        
        # Passo 2: Greedy para o resto
        while len(cobertos) < self.instancia.num_retangulos:
            vertices_disponiveis = [v for v in self.instancia.vertices if v not in guardas]
            if not vertices_disponiveis:
                break
                
            melhor_v = max(vertices_disponiveis, 
                          key=lambda v: len(self.vertice_para_rects[v] - cobertos), 
                          default=None)
                          
            if melhor_v and len(self.vertice_para_rects[melhor_v] - cobertos) > 0:
                guardas.add(melhor_v)
                cobertos.update(self.vertice_para_rects[melhor_v])
            else:
                break
        return guardas

def main():
    print("=" * 70)
    print("ITEM 1 - ESTRATÉGIAS GREEDY")
    print("=" * 70)
    print(f"Instância: {INSTANCIA.num_retangulos} retângulos, {INSTANCIA.num_vertices} vértices")
    print()
    
    solver = EstrategiaGreedy(INSTANCIA)
    estrategias = {
        "E1 - First-Fail": solver.first_fail,
        "E2 - Max Coverage": solver.max_coverage,
        "E3 - Vértices Raros": solver.vertices_raros,
        "E4 - Hierárquica": solver.hierarquica
    }
    
    print("-" * 70)
    print(f"{'Estratégia':<25} {'Guardas':<10} {'Tempo(ms)':<12} {'Solução'}")
    print("-" * 70)
    
    for nome, func in estrategias.items():
        inicio = time.time()
        solucao = func()
        tempo = (time.time() - inicio) * 1000
        
        # Verificar se cobre todos
        cobertos = set()
        for v in solucao:
            cobertos.update(INSTANCIA.retangulos_por_vertice()[v])
        valido = len(cobertos) == INSTANCIA.num_retangulos
        
        print(f"{nome:<25} {len(solucao):<10} {tempo:<12.3f} {sorted(solucao)}")
        if not valido:
            print(f"  ⚠️ ATENÇÃO: Não cobre todos os retângulos!")

if __name__ == "__main__":
    main()