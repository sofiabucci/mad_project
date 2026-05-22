# modelo_matematigo.py
"""
Modelo Matemático do Problema de Cobertura
"""

def exibir_modelo_matematico():
    print("=" * 80)
    print("MODELO MATEMÁTICO DO PROBLEMA")
    print("=" * 80)
    
    print("""
    
    VARIÁVEIS DE DECISÃO:
    ====================
    
    Seja x_i ∈ {0, 1} para i = 1, ..., n, onde n = número de vértices.
    
    x_i = 1  se um guarda é colocado no vértice i
    x_i = 0  caso contrário
    
    
    FUNÇÃO OBJETIVO:
    ===============
    
    Minimizar Z = Σ_{i=1}^{n} x_i
    
    (Minimizar o número total de guardas)
    
    
    RESTRIÇÕES:
    ===========
    
    Para cada retângulo j (j = 1, ..., m), seja V(j) o conjunto de vértices incidentes:
    
    Σ_{i ∈ V(j)} x_i ≥ 1,  ∀ j = 1, ..., m
    
    (Cada retângulo deve ser coberto por pelo menos um guarda)
    
    
    RESTRIÇÕES ADICIONAIS (para a instância específica):
    ====================================================
    
    1. x_1 ≥ 1                    (Retângulo 1: vértice 1)
    2. x_1 + x_2 ≥ 1              (Retângulo 2: vértices 1,2)
    3. x_3 + x_4 ≥ 1              (Retângulo 3: vértices 3,4)
    4. x_2 + x_3 + x_4 + x_5 ≥ 1  (Retângulo 4: vértices 2,3,4,5)
    5. x_5 + x_6 ≥ 1              (Retângulo 5: vértices 5,6)
    6. x_6 + x_7 ≥ 1              (Retângulo 6: vértices 6,7)
    7. x_6 + x_7 + x_8 ≥ 1        (Retângulo 7: vértices 6,7,8)
    8. x_7 + x_8 ≥ 1              (Retângulo 8: vértices 7,8)
    9. x_1 + x_2 + x_3 + x_4 + x_5 ≥ 1  (Retângulo 9: vértices 1,2,3,4,5)
    10. x_8 ≥ 1                   (Retângulo 10: vértice 8)
    
    """)

if __name__ == "__main__":
    exibir_modelo_matematico()