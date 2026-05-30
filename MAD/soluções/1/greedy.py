import sys
import os
import time

# --- REAPROVEITANDO A CLASSE GENÉRICA DO PASSO ANTERIOR ---
class InstanciaGenerica:
    def __init__(self, retangulos_dict, vertices_lista):
        self.retangulos = retangulos_dict
        self.vertices = set(vertices_lista)
        self.num_retangulos = len(retangulos_dict)

    def retangulos_por_vertice(self):
        v_para_r = {v: set() for v in self.vertices}
        for rect_id, verts in self.retangulos.items():
            for v in verts:
                if v in v_para_r:
                    v_para_r[v].add(rect_id)
        return v_para_r

    def verificar_solucao(self, guardas):
        cobertos = set()
        v_para_r = self.retangulos_por_vertice()
        for g in guardas:
            if g in v_para_r:
                cobertos.update(v_para_r[g])
        return len(cobertos) == self.num_retangulos


# --- SUA CLASSE GREEDY (Adaptada para receber a instância) ---
class EstrategiaGreedy:
    def __init__(self, instancia):
        self.instancia = instancia
        self.vertice_para_rects = self.instancia.retangulos_por_vertice()
    
    def first_fail(self):
        guardas, cobertos = set(), set()
        retangulos_ordenados = sorted(self.instancia.retangulos.items(), key=lambda x: len(x[1]))
        while len(cobertos) < self.instancia.num_retangulos:
            alvo = next((r for r in retangulos_ordenados if r[0] not in cobertos), None)
            if not alvo: break
            rect_alvo, verts_alvo = alvo
            melhor_v = max(verts_alvo, key=lambda v: len(self.vertice_para_rects[v] - cobertos), default=None)
            if melhor_v:
                guardas.add(melhor_v)
                cobertos.update(self.vertice_para_rects[melhor_v])
        return guardas
    
    def max_coverage(self):
        guardas, cobertos = set(), set()
        while len(cobertos) < self.instancia.num_retangulos:
            melhor_v, melhor_contagem = None, -1
            for v in self.instancia.vertices:
                if v in guardas: continue
                novos = len(self.vertice_para_rects[v] - cobertos)
                if novos > melhor_contagem:
                    melhor_contagem = novos
                    melhor_v = v
            if melhor_v and melhor_contagem > 0:
                guardas.add(melhor_v)
                cobertos.update(self.vertice_para_rects[melhor_v])
            else: break
        return guardas

    def vertices_raros(self):
        guardas, cobertos = set(), set()
        vertices_ordenados = sorted(self.instancia.vertices, key=lambda v: len(self.vertice_para_rects[v]))
        for v in vertices_ordenados:
            if len(self.vertice_para_rects[v] - cobertos) > 0:
                guardas.add(v)
                cobertos.update(self.vertice_para_rects[v])
        return guardas

    def hierarquica(self):
        guardas, cobertos = set(), set()
        for rect, verts in self.instancia.retangulos.items():
            if len(verts) == 1:
                v = next(iter(verts))
                if v not in guardas:
                    guardas.add(v)
                    cobertos.update(self.vertice_para_rects[v])
        while len(cobertos) < self.instancia.num_retangulos:
            melhor_v = max(self.instancia.vertices - guardas, key=lambda v: len(self.vertice_para_rects[v] - cobertos), default=None)
            if melhor_v and len(self.vertice_para_rects[melhor_v] - cobertos) > 0:
                guardas.add(melhor_v)
                cobertos.update(self.vertice_para_rects[melhor_v])
            else: break
        return guardas


# --- PARSER DO FICHEIRO GERADO PELO C ---
def carregar_instancias_do_c(caminho_arquivo):
    """
    Lê o arquivo de resultados do rectParts.c e converte
    para objetos da classe InstanciaGenerica.
    """
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        sys.exit(1)

    with open(caminho_arquivo, 'r') as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]
    
    if not linhas:
        return []

    num_instancias = int(linhas[0])
    idx = 1
    instancias_processadas = []

    for _ in range(num_instancias):
        if idx >= len(linhas): break
        
        num_faces = int(linhas[idx])
        idx += 1
        
        retangulos_dict = {}
        todos_vertices = set()
        
        for _ in range(num_faces):
            partes = list(map(int, linhas[idx].split()))
            idx += 1
            
            face_id = partes[0]
            num_verts = partes[1]
            
            # Agrupa os números de 2 em 2 para formar tuplas de coordenadas (X, Y)
            coords_linha = partes[2:]
            vertices_face = []
            for i in range(num_verts):
                x = coords_linha[2 * i]
                y = coords_linha[2 * i + 1]
                v_tupla = (x, y) # Usar coordenadas como ID único do vértice
                vertices_face.append(v_tupla)
                todos_vertices.add(v_tupla)
                
            retangulos_dict[f"Face_{face_id}"] = set(vertices_face)
            
        instancias_processadas.append(InstanciaGenerica(retangulos_dict, list(todos_vertices)))
        
    return instancias_processadas


# --- EXECUÇÃO PRINCIPAL ---
def main():
    if len(sys.argv) < 2:
        print("Uso: python solver_dcel.py <arquivo_resultados_do_c.txt>")
        sys.exit(1)
        
    arquivo_c = sys.argv[1]
    instancias = carregar_instancias_do_c(arquivo_c)
    
    print(f"Foram carregadas {len(instancias)} instâncias do arquivo.")
    
    for i, inst in enumerate(instancias, 1):
        print("\n" + "=" * 80)
        print(f" RESOLVENDO INSTÂNCIA CRIADA PELO PROGRAMA C #{i}")
        print("=" * 80)
        print(f"Total de Retângulos (Faces): {inst.num_retangulos} | Vértices Únicos detetados: {len(inst.vertices)}")
        
        solver = EstrategiaGreedy(inst)
        estrategias = {
            "E1 - First-Fail": solver.first_fail,
            "E2 - Max Coverage": solver.max_coverage,
            "E3 - Vértices Raros": solver.vertices_raros,
            "E4 - Hierárquica": solver.hierarquica
        }
        
        print("-" * 80)
        print(f"{'Estratégia':<25} {'Guardas':<10} {'Tempo(ms)':<12} {'Validação'}")
        print("-" * 80)
        
        for nome, func in list(estrategias.items()):
            inicio = time.time()
            solucao = func()
            tempo = (time.time() - inicio) * 1000
            valida = "✓ Válida" if inst.verificar_solucao(solucao) else "✗ Falhou"
            
            print(f"{nome:<25} {len(solucao):<10} {tempo:<12.3f} {valida}")
            # Se quiser ver as coordenadas dos guardas escolhidos, descomente a linha abaixo:
            # print(f"   > Guardas em: {sorted(solucao)}")

if __name__ == "__main__":
    main()