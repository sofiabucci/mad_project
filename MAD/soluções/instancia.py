"""
Instância única do problema - 8 vértices, 10 retângulos
Baseada na tabela do enunciado do trabalho
"""

class InstanciaParticao:
    def __init__(self):
        # Retângulos e seus vértices incidentes (conforme tabela)
        self.retangulos = {
            1: {1},                      # R1: vértice 1
            2: {1, 2},                   # R2: vértices 1,2
            3: {3, 4},                   # R3: vértices 3,4
            4: {2, 3, 4, 5},             # R4: vértices 2,3,4,5
            5: {5, 6},                   # R5: vértices 5,6
            6: {6, 7},                   # R6: vértices 6,7
            7: {6, 7, 8},                # R7: vértices 6,7,8
            8: {7, 8},                   # R8: vértices 7,8
            9: {1, 2, 3, 4, 5},          # R9: vértices 1,2,3,4,5
            10: {8}                      # R10: vértice 8
        }
        
        self.vertices = list(range(1, 9))
        self.num_retangulos = len(self.retangulos)
        self.num_vertices = len(self.vertices)
    
    def retangulos_por_vertice(self):
        """Mapeia cada vértice para os retângulos que ele cobre"""
        mapa = {v: set() for v in self.vertices}
        for rect, verts in self.retangulos.items():
            for v in verts:
                mapa[v].add(rect)
        return mapa
    
    def solucoes_optimas(self):
        """Soluções ótimas conhecidas para validação"""
        return [
            {1, 3, 5, 8},
            {1, 3, 6, 8},
            {1, 4, 5, 8},
            {1, 4, 6, 8}
        ]
    
    def verificar_solucao(self, guardas):
        """Verifica se uma solução cobre todos os retângulos"""
        cobertos = set()
        for v in guardas:
            cobertos.update(self.retangulos_por_vertice()[v])
        return len(cobertos) == self.num_retangulos
    
    def __str__(self):
        """Representação textual da instância"""
        s = "Instância do Problema:\n"
        s += f"  Vértices: {self.vertices}\n"
        s += f"  Número de vértices: {self.num_vertices}\n"
        s += f"  Número de retângulos: {self.num_retangulos}\n"
        s += "\n  Retângulos e vértices incidentes:\n"
        for rect, verts in sorted(self.retangulos.items()):
            s += f"    R{rect}: {sorted(verts)} (tamanho={len(verts)})\n"
        return s


# Instância global para uso em todos os módulos
INSTANCIA = InstanciaParticao()