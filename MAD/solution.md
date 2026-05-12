# Solução: Cobertura de Partições Retangulares

## a) Relação entre a estratégia *greedy* e *first-fail*

- A estratégia *greedy* do enunciado escolhe primeiro o retângulo com menos nós incidentes.
- Esse retângulo é o mais restrito: ele tem menos vértices candidatos para colocar um guarda.
- Em CSPs, a heurística *first-fail* seleciona primeiro a variável com o menor domínio, ou seja, a escolha mais limitada.
- A relação é direta: ambos priorizam o elemento mais restritivo para reduzir rapidamente o espaço de busca e evitar decisões tardias que podem ser inviáveis.
- No problema de guardas, tratar primeiro o retângulo com menos vértices incidentes equivale a forçar cedo a cobertura das áreas mais difíceis.

## b) Por que descartar os nós externos ainda preserva alguma solução ótima

- A instância possui um retângulo maior e um conjunto de vértices na borda externa desse retângulo.
- Esses vértices externos cobrem principalmente retângulos do contorno.
- Se para a instância existe uma solução ótima que usa apenas vértices internos ou vértices na borda interna, então remover os vértices externos não elimina todas as soluções ótimas.
- No caso em estudo, há conjuntos de guardas ótimos que não dependem de nenhum vértice estritamente externo ao retângulo maior.
- Portanto, descartar os nós externos reduz a busca sem descartar todas as soluções ótimas, porque um conjunto equivalente de vértices internos é capaz de cobrir todas as peças.

## c) Programa para resolver a instância

### Modelo de solução

- Variáveis binárias:
  - `x[i] = 1` se houver guarda no vértice `i`.
  - `x[i] = 0` caso contrário.
- Objetivo:
  - Minimizar `x[1] + x[2] + ... + x[8]`.
- Restrições:
  - Cada retângulo da instância deve ser coberto por pelo menos um guarda em um de seus vértices incidentes.
  - O arquivo `partsRects.py` define 10 restrições que representam os 10 retângulos da partição.

### Resultado exato para a instância

- Valor ótimo: **4 guardas**.
- Soluções ótimas encontradas para os vértices:
  - `{1, 3, 5, 8}`
  - `{1, 3, 6, 8}`
  - `{1, 4, 5, 8}`
  - `{1, 4, 6, 8}`

Essas quatro soluções são equivalentes em custo e cobrem todas as peças da instância.

### Sobre o código

- O arquivo `partsRects.py` agora tenta usar `OR-Tools` com o solver `SCIP`.
- Se `OR-Tools` não estiver instalado ou se `SCIP` não estiver disponível, o script faz uma busca por força bruta e continua encontrando o resultado ótimo.
- Isso garante que a solução seja obtida mesmo sem dependências externas.

### Como executar

1. Instale `OR-Tools` se desejar usar o solver MIP:

```bash
pip install ortools
```

2. Execute:

```bash
cd /home/sofiabucci/mad_project/MAD
python3 partsRects.py
```

3. Se não tiver `OR-Tools`, o script exibirá a mensagem de fallback e ainda retornará o resultado ótimo.

### Exemplo de saída

```text
Optimal cost: 4
Optimal guard placements:
  (1, 3, 5, 8)
  (1, 3, 6, 8)
  (1, 4, 5, 8)
  (1, 4, 6, 8)
```

## Conclusão

- `a)` A heurística *greedy* por retângulo menos incidente é análoga ao *first-fail* porque ambas escolhem primeiro a parte mais restritiva.
- `b)` Para a instância dada, descartar nós externos pode preservar uma solução ótima quando existe uma cobertura completa usando vértices internos ou borda interna.
- `c)` O script `partsRects.py` resolve a instância e mostra que o número mínimo de guardas é **4**.
