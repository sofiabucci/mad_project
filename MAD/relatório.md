# Relatório do Trabalho MAD 2025/2026

## Cobertura de Partições Retangulares

## Apresentação do Problema

O problema de vigilância de partições retangulares consiste em colocar guardas nos vértices de uma partição retangular, de forma que cada retângulo (peça) seja "visto" por pelo menos um guarda num dos seus vértices.

Neste trabalho, consideramos uma instância específica com:
- **8 vértices** (numerados de 1 a 8)
- **10 retângulos** (peças)

### Retângulos e Vértices Incidentes

| Retângulo | Vértices Incidentes | Tamanho |
|-----------|--------------------|---------|
| 1 | {1} | 1 |
| 2 | {1, 2} | 2 |
| 3 | {3, 4} | 2 |
| 4 | {2, 3, 4, 5} | 4 |
| 5 | {5, 6} | 2 |
| 6 | {6, 7} | 2 |
| 7 | {6, 7, 8} | 3 |
| 8 | {7, 8} | 2 |
| 9 | {1, 2, 3, 4, 5} | 5 |
| 10 | {8} | 1 |

### Soluções Ótimas Conhecidas


## Item 1 - Avaliação de Estratégias Greedy

### Descrição

Foram implementadas quatro estratégias greedy para obter uma colocação dos guardas que garanta a cobertura pedida.

### Estratégias Implementadas

| Estratégia | Descrição |
|------------|-----------|
| **E1 - First-Fail** | Escolher o retângulo com menos vértices incidentes primeiro |
| **E2 - Max Coverage** | Escolher o vértice que cobre mais retângulos não cobertos |
| **E3 - Vértices Raros** | Escolher o vértice que aparece em menos retângulos |
| **E4 - Hierárquica** | Colocar guardas nos vértices obrigatórios primeiro, depois aplicar greedy |

### Relação com First-Fail (CSPs)

A estratégia E1 é a aplicação direta do princípio **first-fail** dos CSPs:

| First-Fail em CSPs | Estratégia Greedy E1 |
|--------------------|---------------------|
| Variável com menor domínio | Retângulo com menos vértices |
| Falhar cedo (fail early) | Decisão crítica primeiro |
| Reduz o espaço de busca | Evita backtracking excessivo |

### Resultados

| Estratégia | Guardas | Tempo (ms) | Solução | Ótima? |
|------------|---------|------------|---------|--------|
| E1 - First-Fail | _ | _ | _ | _ |
| E2 - Max Coverage | _ | _ | _ | _ |
| E3 - Vértices Raros | _ | _ | _ | _ |
| E4 - Hierárquica | _ | _ | _ | _ |

---

## Item 2 - Programação Inteira e Programação por Restrições

### Item 2a - Modelo Matemático

#### Variáveis de Decisão

Seja \( x_i \in \{0, 1\} \) para \( i = 1, 2, ..., 8 \), onde:
- \( x_i = 1 \) se um guarda é colocado no vértice \( i \)
- \( x_i = 0 \) caso contrário

#### Função Objetivo

Minimizar o número total de guardas:

\[
\text{Minimizar} \quad Z = \sum_{i=1}^{8} x_i
\]

#### Restrições

Para cada retângulo \( j \), a soma dos vértices incidentes deve ser ≥ 1:

| Retângulo | Restrição |
|-----------|-----------|
| 1 | \( x_1 \geq 1 \) |
| 2 | \( x_1 + x_2 \geq 1 \) |
| 3 | \( x_3 + x_4 \geq 1 \) |
| 4 | \( x_2 + x_3 + x_4 + x_5 \geq 1 \) |
| 5 | \( x_5 + x_6 \geq 1 \) |
| 6 | \( x_6 + x_7 \geq 1 \) |
| 7 | \( x_6 + x_7 + x_8 \geq 1 \) |
| 8 | \( x_7 + x_8 \geq 1 \) |
| 9 | \( x_1 + x_2 + x_3 + x_4 + x_5 \geq 1 \) |
| 10 | \( x_8 \geq 1 \) |

#### Domínio

\[
x_i \in \{0, 1\}, \quad \forall i = 1, \ldots, 8
\]

### Item 2b - Propagação de Restrições (MAC com AC-3)

Foi implementado um resolvedor **sem recorrer a módulos de programação por restrições**, aplicando:

- **AC-3 (Arc Consistency 3):** algoritmo que mantém a consistência de arcos entre variáveis e restrições
- **MAC (Maintaining Arc Consistency):** backtracking com manutenção da consistência de arcos após cada atribuição
- **Heurística First-Fail:** escolher a variável com menor domínio
- **Heurística LCV (Least Constraining Value):** ordenar valores por impacto (menos eliminações primeiro)

#### Algoritmo AC-3

```
Função AC-3(fila):
    enquanto fila não vazia:
        (var, rest) ← remover primeiro da fila
        se revisar(var, rest) então
            se domínio[var] vazio então
                retornar FALSO
            para cada (var2, rest2) com var2 ≠ var e var em rest2:
                adicionar (var2, rest2) à fila
    retornar VERDADEIRO
```

#### Resultados

| Métrica | Valor |
|---------|-------|
| Tempo de execução | _ ms |
| Nós explorados | _ |
| Poda realizada | _ |
| Guardas | _ |
| Custo | _ |

### Item 2c - Resolução em SWI-Prolog (CLPFD)

```prolog
:- use_module(library(clpfd)).

retangulo(1, [1]).
retangulo(2, [1,2]).
retangulo(3, [3,4]).
retangulo(4, [2,3,4,5]).
retangulo(5, [5,6]).
retangulo(6, [6,7]).
retangulo(7, [6,7,8]).
retangulo(8, [7,8]).
retangulo(9, [1,2,3,4,5]).
retangulo(10, [8]).

coberto(Vertices, Vars) :-
    maplist({Vars}/[I, X]>>(nth1(I, Vars, X)), Vertices, VarsRet),
    sum(VarsRet, #>=, 1).

resolver(Guardas, Total) :-
    length(Vars, 8),
    Vars ins 0..1,
    findall(R, retangulo(R, _), Retangulos),
    todos_cobertos(Retangulos, Vars),
    sum(Vars, #=, Total),
    labeling([min(Total)], Vars),
    findall(I, (nth1(I, Vars, 1)), Guardas).
```

#### Resultados

| Métrica | Valor |
|---------|-------|
| Tempo de execução | _ ms |
| Guardas | _ |
| Custo | _ |

### Item 2c - Resolução em Google OR-Tools

```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()
x = {i: model.NewBoolVar(f'x_{i}') for i in range(1, 9)}

# Restrições
model.Add(x[1] >= 1)
model.Add(x[1] + x[2] >= 1)
model.Add(x[3] + x[4] >= 1)
model.Add(x[2] + x[3] + x[4] + x[5] >= 1)
model.Add(x[5] + x[6] >= 1)
model.Add(x[6] + x[7] >= 1)
model.Add(x[6] + x[7] + x[8] >= 1)
model.Add(x[7] + x[8] >= 1)
model.Add(x[1] + x[2] + x[3] + x[4] + x[5] >= 1)
model.Add(x[8] >= 1)

model.Minimize(sum(x[i] for i in range(1, 9)))
```

#### Resultados

| Método | Guardas | Tempo (ms) |
|--------|---------|------------|
| CP-SAT | _ | _ |
| MIP (SCIP) | _ | _ |

---

## Item 3 - Avaliação de Programação Dinâmica

### Descrição

A programação dinâmica resolve o problema dividindo-o em subproblemas menores, onde cada estado representa um subconjunto de retângulos já cobertos.

### Definição dos Estados

- **Máscara de bits:** cada retângulo é representado por um bit (1 a 10)
- **Estado:** dp[mask] = melhor custo para cobrir os retângulos em mask
- **Transição:** dp[mask | mask_v] = min(dp[mask | mask_v], dp[mask] + 1)

### Algoritmo

```
Função ProgramacaoDinamica():
    dp[0] = (0, conjunto_vazio)
    
    para mask_atual de 0 a 2^n - 1:
        se mask_atual não está em dp:
            continue
        
        (custo_atual, vertices) = dp[mask_atual]
        
        para cada vértice v:
            nova_mask = mask_atual | mascara_do_vertice[v]
            novo_custo = custo_atual + 1
            
            se nova_mask não está em dp:
                dp[nova_mask] = (novo_custo, vertices ∪ {v})
            senão se novo_custo < dp[nova_mask].custo:
                dp[nova_mask] = (novo_custo, vertices ∪ {v})
    
    retornar dp[mask_completa]
```

### Complexidade

| Métrica | Valor |
|---------|-------|
| Número de retângulos (n) | 10 |
| Número de vértices (m) | 8 |
| Estados (2^n) | 1024 |
| Operações | 8192 |
| Complexidade de espaço | O(2^n × m) |
| Complexidade de tempo | O(2^n × m) |

### Resultados

| Abordagem | Tempo (ms) | Guardas | Solução |
|-----------|------------|---------|---------|
| DP com tabela (bottom-up) | _ | _ | _ |
| DP com memoização (top-down) | _ | _ | _ |

---

## Item 4 - Extensões do Problema

### Item 4a - Guardas com Cores

#### Descrição

Guardas que veem o mesmo retângulo devem ter cores distintas. Pretende-se:
1. Minimizar o número de guardas
2. Para o número mínimo de guardas, determinar o número mínimo de cores

#### Modelo Adicional

Além das variáveis originais \( x_i \), introduzem-se:
- Variáveis de cor: \( c_i \in \{1, \ldots, k\} \) para cada guarda colocado
- Restrição de conflito: se os vértices \( u \) e \( v \) cobrem o mesmo retângulo, então \( c_u \neq c_v \)

#### Resultados

| Métrica | Valor |
|---------|-------|
| Número mínimo de guardas | _ |
| Número mínimo de cores | _ |
| Guardas | _ |
| Distribuição de cores | _ |

### Item 4b - Guardas com Maior Alcance

#### Descrição

Um guarda num vértice pode guardar não só os retângulos incidentes, mas também retângulos vizinhos a uma distância \( D \) no grafo de adjacência (com \( D \) dado como parâmetro).

#### Construção do Grafo

- **Nós:** vértices da partição (1 a 8)
- **Arestas:** conectam dois vértices se eles cobrem o mesmo retângulo

#### Cálculo do Alcance

Para um dado \( D \), o alcance de um vértice é calculado por BFS até profundidade \( D \).

#### Resultados

| Distância D | Guardas Mínimos | Solução |
|-------------|-----------------|---------|
| D = 1 | _ | _ |
| D = 2 | _ | _ |
| D = 3 | _ | _ |

---

## Conclusões

### Resumo dos Resultados

| Abordagem | Guardas | Tempo (ms) |
|-----------|---------|------------|
| Greedy (E4 - Hierárquica) | _ | _ |
| MAC + AC-3 | _ | _ |
| SWI-Prolog CLPFD | _ | _ |
| OR-Tools CP-SAT | _ | _ |
| Programação Dinâmica | _ | _ |
| Guardas com Cores | _ guardas, _ cores | - |
| Guardas com Alcance D=2 | _ | - |

### Soluções Ótimas

