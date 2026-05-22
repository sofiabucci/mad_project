# constraint_propagation.py
"""
Implementação de propagação de restrições (MAC + AC-3)
Sem usar módulos de programação por restrições
"""

from typing import Set, Dict, List, Tuple, Optional
from collections import deque
import time

class PropagacaoRestricoes:
    """
    Implementa Maintaining Arc Consistency (MAC) com AC-3
    """
    
    def __init__(self, instancia):
        self.instancia = instancia
        self.vertices = instancia.vertices
        self.retangulos = instancia.retangulos
        self.num_vertices = len(self.vertices)
        self.num_retangulos = len(self.retangulos)
        
        # Domínios: cada vértice pode ser 0 ou 1
        self.dominios = {v: {0, 1} for v in self.vertices}
        
        # Restrições: para cada retângulo, a soma dos vértices >= 1
        self.restricoes = []
        for rect, verts in self.retangulos.items():
            self.restricoes.append(('sum_ge', list(verts), 1))
        
        # Histórico para backtracking
        self.historico = []
    
    # ============================================================
    # AC-3: Manutenção de Arc Consistency
    # ============================================================
    
    def arco_consistente(self, variavel: int, valor: int, restricao: Tuple) -> bool:
        """
        Verifica se atribuir `valor` à `variavel` é consistente com a restrição
        """
        tipo, vars_list, limiar = restricao
        
        if tipo == 'sum_ge':
            if variavel not in vars_list:
                return True
            
            # Simplificação: para a restrição Σ x_i ≥ 1
            # Se a variável atual for 0, ainda é possível satisfazer se outras forem 1
            # Se a variável atual for 1, a restrição é satisfeita independentemente
            if valor == 1:
                return True
            else:  # valor == 0
                # Verificar se ainda há pelo menos uma outra variável que pode ser 1
                outras_possibilidades = False
                for v in vars_list:
                    if v != variavel:
                        if 1 in self.dominios[v]:
                            outras_possibilidades = True
                            break
                return outras_possibilidades
        
        return True
    
    def revisar(self, variavel: int, restricao: Tuple) -> bool:
        """
        Revisa o domínio da variável com base na restrição
        Retorna True se o domínio foi modificado
        """
        tipo, vars_list, limiar = restricao
        
        if variavel not in vars_list:
            return False
        
        modificado = False
        valores_remover = []
        
        for valor in self.dominios[variavel]:
            if not self.arco_consistente(variavel, valor, restricao):
                valores_remover.append(valor)
        
        for valor in valores_remover:
            self.dominios[variavel].remove(valor)
            modificado = True
        
        return modificado
    
    def ac3(self, fila_inicial: Optional[List[Tuple]] = None) -> bool:
        """
        Algoritmo AC-3 para manter arc consistency
        """
        if fila_inicial is None:
            # Inicializar com todos os arcos (variável, restrição)
            fila = deque()
            for v in self.vertices:
                for r in self.restricoes:
                    if v in r[1]:
                        fila.append((v, r))
        else:
            fila = deque(fila_inicial)
        
        while fila:
            var, rest = fila.popleft()
            if self.revisar(var, rest):
                if len(self.dominios[var]) == 0:
                    return False  # Inconsistência
                # Adicionar arcos vizinhos de volta à fila
                for outra_rest in self.restricoes:
                    if outra_rest != rest and var in outra_rest[1]:
                        for outra_var in outra_rest[1]:
                            if outra_var != var:
                                fila.append((outra_var, outra_rest))
        return True
    
    # ============================================================
    # Heurísticas
    # ============================================================
    
    def first_fail(self) -> Optional[int]:
        """
        Heurística first-fail: escolher variável com menor domínio
        """
        melhor_var = None
        menor_dominio = float('inf')
        
        for v in self.vertices:
            if len(self.dominios[v]) > 1:  # Não fixa
                if len(self.dominios[v]) < menor_dominio:
                    menor_dominio = len(self.dominios[v])
                    melhor_var = v
        
        return melhor_var
    
    def least_constraining_value(self, var: int) -> List[int]:
        """
        Heurística LCV: ordenar valores por quantas restrições eliminam
        """
        valores = list(self.dominios[var])
        
        def contagem_eliminacoes(valor):
            eliminacoes = 0
            for rest in self.restricoes:
                if var in rest[1]:
                    if not self.arco_consistente(var, valor, rest):
                        eliminacoes += 1
            return eliminacoes
        
        return sorted(valores, key=contagem_eliminacoes)
    
    # ============================================================
    # Backtracking com MAC
    # ============================================================
    
    def guardar_estado(self):
        """Guarda o estado atual dos domínios"""
        estado = {v: self.dominios[v].copy() for v in self.vertices}
        self.historico.append(estado)
    
    def restaurar_estado(self):
        """Restaura o estado anterior dos domínios"""
        if self.historico:
            self.dominios = self.historico.pop()
    
    def propagar(self, var: int, valor: int) -> bool:
        """
        Propaga a atribuição (var = valor) usando AC-3
        """
        # Salvar estado
        self.guardar_estado()
        
        # Fixar o valor
        self.dominios[var] = {valor}
        
        # Criar fila inicial com arcos afetados
        fila = []
        for rest in self.restricoes:
            if var in rest[1]:
                for outra_var in rest[1]:
                    if outra_var != var:
                        fila.append((outra_var, rest))
        
        # Executar AC-3
        if self.ac3(fila):
            return True
        else:
            self.restaurar_estado()
            return False
    
    def solucao_parcial_valida(self) -> bool:
        """
        Verifica se a solução parcial é válida
        """
        for rest in self.restricoes:
            tipo, vars_list, limiar = rest
            if tipo == 'sum_ge':
                # Se todas as variáveis já estão fixadas em 0, é inválido
                soma_possivel = False
                for v in vars_list:
                    if 1 in self.dominios[v]:
                        soma_possivel = True
                        break
                if not soma_possivel:
                    return False
        return True
    
    def backtrack(self) -> Optional[Dict[int, int]]:
        """
        Backtracking com MAC (Maintaining Arc Consistency)
        """
        # Verificar solução parcial
        if not self.solucao_parcial_valida():
            return None
        
        # Verificar se todas as variáveis estão fixadas
        todas_fixadas = all(len(self.dominios[v]) == 1 for v in self.vertices)
        
        if todas_fixadas:
            # Construir solução
            solucao = {v: next(iter(self.dominios[v])) for v in self.vertices}
            return solucao
        
        # First-fail: escolher variável com menor domínio
        var = self.first_fail()
        if var is None:
            return None
        
        # LCV: ordenar valores
        valores = self.least_constraining_value(var)
        
        for valor in valores:
            if self.propagar(var, valor):
                resultado = self.backtrack()
                if resultado is not None:
                    return resultado
            # Se falhou, restaurar estado já foi feito em propagar
        
        return None
    
    def resolver(self) -> Tuple[Optional[Set[int]], int]:
        """
        Resolve o problema usando MAC + AC-3
        """
        print("\n" + "=" * 80)
        print("RESOLUÇÃO COM PROPAGAÇÃO DE RESTRIÇÕES (MAC + AC-3)")
        print("=" * 80)
        
        inicio = time.time()
        
        # Inicializar domínios
        self.dominios = {v: {0, 1} for v in self.vertices}
        self.historico = []
        
        # Aplicar AC-3 inicial
        if not self.ac3():
            print("Problema inconsistente desde o início!")
            return None, 0
        
        # Backtracking com MAC
        solucao_parcial = self.backtrack()
        
        tempo = time.time() - inicio
        
        if solucao_parcial:
            guardas = {v for v, val in solucao_parcial.items() if val == 1}
            print(f"\nSolução encontrada em {tempo:.4f} segundos")
            print(f"Guardas: {sorted(guardas)}")
            print(f"Número de guardas: {len(guardas)}")
            return guardas, len(guardas)
        else:
            print(f"\nNenhuma solução encontrada em {tempo:.4f} segundos")
            return None, 0

# Teste da implementação
if __name__ == "__main__":
    from rect_coverage_solver import InstanciaParticao
    
    instancia = InstanciaParticao()
    solver = PropagacaoRestricoes(instancia)
    guardas, custo = solver.resolver()