"""
ITEM 2b - Propagação de Restrições (MAC + AC-3)
Semusar módulos de programação por restrições

Implementação completa de:
- AC-3 (Arc Consistency 3)
- MAC (Maintaining Arc Consistency)
- Heurísticas: First-Fail, LCV (Least Constraining Value)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from instancia import INSTANCIA
from collections import deque
import time
from typing import Set, Dict, List, Tuple, Optional

class AC3_MAC:
    """
    Implementação de Maintaining Arc Consistency com AC-3
    """
    
    def __init__(self, instancia=None):
        self.instancia = instancia or INSTANCIA
        self.vertices = self.instancia.vertices
        self.num_vertices = len(self.vertices)
        
        # Domínios: cada vértice pode ser 0 ou 1
        self.dominios = {v: {0, 1} for v in self.vertices}
        
        # Restrições: para cada retângulo, soma dos vértices >= 1
        self.restricoes = []
        for rect, verts in self.instancia.retangulos.items():
            self.restricoes.append({
                'tipo': 'sum_ge',
                'vars': list(verts),
                'limiar': 1,
                'id': rect
            })
        
        self.historico = []  # Para backtracking
        self.contador_nos = 0
        self.contador_poda = 0
    
    # ============================================================
    # AC-3: Arc Consistency 3
    # ============================================================
    
    def _consistente(self, var: int, valor: int, rest: Dict) -> bool:
        """
        Verifica se a atribuição (var=valor) é consistente com a restrição
        """
        if var not in rest['vars']:
            return True
        
        # Para restrição Σ x_i ≥ 1
        if valor == 1:
            return True  # Guarda satisfaz a restrição
        else:  # valor == 0
            # Verificar se outra variável pode ser 1
            for v in rest['vars']:
                if v != var and 1 in self.dominios[v]:
                    return True
            return False
    
    def _revisar(self, var: int, rest: Dict) -> bool:
        """
        Revisa o domínio de var com base na restrição
        Retorna True se o domínio foi reduzido
        """
        if var not in rest['vars']:
            return False
        
        modificado = False
        valores_remover = []
        
        for val in self.dominios[var]:
            if not self._consistente(var, val, rest):
                valores_remover.append(val)
        
        for val in valores_remover:
            self.dominios[var].remove(val)
            modificado = True
            self.contador_poda += 1
        
        return modificado
    
    def ac3(self, fila_inicial: Optional[List] = None) -> bool:
        """
        Algoritmo AC-3
        Mantém a consistência de arcos entre variáveis e restrições
        """
        if fila_inicial is None:
            fila = deque()
            for v in self.vertices:
                for r in self.restricoes:
                    if v in r['vars']:
                        fila.append((v, r))
        else:
            fila = deque(fila_inicial)
        
        while fila:
            var, rest = fila.popleft()
            if self._revisar(var, rest):
                if len(self.dominios[var]) == 0:
                    return False  # Inconsistência
                # Adicionar arcos vizinhos
                for outra_rest in self.restricoes:
                    if outra_rest != rest and var in outra_rest['vars']:
                        for outra_var in outra_rest['vars']:
                            if outra_var != var:
                                fila.append((outra_var, outra_rest))
        return True
    
    # ============================================================
    # Heurísticas
    # ============================================================
    
    def first_fail(self) -> Optional[int]:
        """
        First-Fail: escolher variável com menor domínio (>1)
        """
        melhor_var = None
        menor_dominio = float('inf')
        
        for v in self.vertices:
            tam = len(self.dominios[v])
            if 1 < tam < menor_dominio:
                menor_dominio = tam
                melhor_var = v
        
        return melhor_var
    
    def least_constraining_value(self, var: int) -> List[int]:
        """
        LCV: ordenar valores por menos eliminações
        """
        def impacto(valor):
            count = 0
            for rest in self.restricoes:
                if var in rest['vars']:
                    if not self._consistente(var, valor, rest):
                        count += 1
            return count
        
        return sorted(self.dominios[var], key=impacto)
    
    # ============================================================
    # Backtracking com MAC
    # ============================================================
    
    def _guardar_estado(self):
        self.historico.append({v: self.dominios[v].copy() for v in self.vertices})
    
    def _restaurar_estado(self):
        if self.historico:
            self.dominios = self.historico.pop()
    
    def _propagar(self, var: int, valor: int) -> bool:
        """
        Propaga a atribuição (var=valor) usando AC-3
        """
        self._guardar_estado()
        self.dominios[var] = {valor}
        
        # Filtrar arcos afetados
        fila = []
        for rest in self.restricoes:
            if var in rest['vars']:
                for outra_var in rest['vars']:
                    if outra_var != var:
                        fila.append((outra_var, rest))
        
        if self.ac3(fila):
            return True
        else:
            self._restaurar_estado()
            return False
    
    def _solucao_parcial_valida(self) -> bool:
        """
        Verifica se a solução parcial ainda pode levar a uma solução válida
        """
        for rest in self.restricoes:
            # Se todas as variáveis estão fixadas em 0, é inválido
            todas_zero = True
            for v in rest['vars']:
                if len(self.dominios[v]) == 1:
                    if next(iter(self.dominios[v])) == 1:
                        todas_zero = False
                        break
                else:
                    todas_zero = False
                    break
            if todas_zero:
                return False
        return True
    
    def _backtrack(self) -> Optional[Dict[int, int]]:
        """
        Backtracking recursivo com MAC
        """
        self.contador_nos += 1
        
        if not self._solucao_parcial_valida():
            return None
        
        # Verificar se todas as variáveis estão fixadas
        if all(len(self.dominios[v]) == 1 for v in self.vertices):
            return {v: next(iter(self.dominios[v])) for v in self.vertices}
        
        var = self.first_fail()
        if var is None:
            return None
        
        for valor in self.least_constraining_value(var):
            if self._propagar(var, valor):
                resultado = self._backtrack()
                if resultado is not None:
                    return resultado
        
        return None
    
    def resolver(self) -> Tuple[Optional[Set[int]], int, int, int]:
        """
        Resolve o problema usando MAC + AC-3
        """
        print("\n" + "=" * 70)
        print("ITEM 2b - PROPAGAÇÃO DE RESTRIÇÕES (MAC + AC-3)")
        print("=" * 70)
        
        inicio = time.time()
        
        self.dominios = {v: {0, 1} for v in self.vertices}
        self.historico = []
        self.contador_nos = 0
        self.contador_poda = 0
        
        # AC-3 inicial
        if not self.ac3():
            print("Problema inconsistente!")
            return None, 0, 0, 0
        
        # Backtracking com MAC
        solucao_dict = self._backtrack()
        
        tempo = (time.time() - inicio) * 1000
        
        if solucao_dict:
            guardas = {v for v, val in solucao_dict.items() if val == 1}
            print(f"\n✓ Solução encontrada!")
            print(f"  • Tempo: {tempo:.3f} ms")
            print(f"  • Nós explorados: {self.contador_nos}")
            print(f"  • Poda realizada: {self.contador_poda}")
            print(f"  • Guardas: {sorted(guardas)}")
            print(f"  • Número: {len(guardas)}")
            return guardas, len(guardas), self.contador_nos, tempo
        else:
            print(f"\n✗ Nenhuma solução encontrada")
            return None, 0, self.contador_nos, tempo


def main():
    solver = AC3_MAC()
    guardas, custo, nos, tempo = solver.resolver()
    
    if guardas and INSTANCIA.verificar_solucao(guardas):
        print(f"\n✓ Validação: todos os {INSTANCIA.num_retangulos} retângulos cobertos")
        
        # Verificar se é ótima
        custo_otimo = len(INSTANCIA.solucoes_optimas()[0])
        if custo == custo_otimo:
            print(f"✓ Solução ótima (custo = {custo_otimo})")
        else:
            print(f"✗ Solução subótima (ótimo = {custo_otimo})")


if __name__ == "__main__":
    main()