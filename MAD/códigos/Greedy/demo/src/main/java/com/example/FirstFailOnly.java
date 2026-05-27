package com.example;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

class Rectangle {
    int id;
    List<String> vertices;

    Rectangle(int id, String... v) {
        this.id = id;
        this.vertices = Arrays.asList(v);
    }
}

public class FirstFailOnly {

    public static void main(String[] args) {

        /*
            MAPA DE REFERÊNCIA
            A----B----C-----------D----E
            | R4 | R3 |           |    |
            F----G----H           |    |
            |   R5    |           |    |
            I---------J    R2     |    |
            |   R6    |           | R1 |
            K---------L-----------M    |
            |   R7                |    |
            N----O----------------P    |
            |R9  |                |    |
            Q----R                |    |
            |R10 |R8              |    |
            S----T----------------U----V
        */

        List<Rectangle> rects = new ArrayList<>();

        rects.add(new Rectangle(1, "D", "E", "M", "P", "U", "V"));
        rects.add(new Rectangle(2, "C", "D", "H", "J", "L", "M"));
        rects.add(new Rectangle(3, "B", "C", "H", "G"));
        rects.add(new Rectangle(4, "A", "B", "G", "F"));
        rects.add(new Rectangle(5, "F", "G", "H", "J", "I"));
        rects.add(new Rectangle(6, "I", "J", "L", "K"));
        rects.add(new Rectangle(7, "K", "L", "M", "P", "O", "N"));
        rects.add(new Rectangle(8, "O", "P", "U", "T", "R"));
        rects.add(new Rectangle(9, "N", "O", "R", "Q"));
        rects.add(new Rectangle(10, "Q", "R", "T", "S"));

        Set<Integer> covered = new HashSet<>();
        Set<String> guards = new LinkedHashSet<>();

        /*
            ESTRATÉGIA: FIRST-FAIL PURA
            
            1. Encontra o retângulo mais restrito (com menos vértices livres de guardas).
            2. Escolhe o primeiro vértice disponível dele, sem olhar para a vizinhança.
        */
        while (covered.size() < rects.size()) {

            Rectangle rarestRectangle = null;
            int minAvailableVertices = Integer.MAX_VALUE;

            // 1. PASSO FIRST-FAIL: Achar o retângulo mais crítico
            for (Rectangle r : rects) {
                if (covered.contains(r.id)) continue;

                // Contar quantos vértices deste retângulo ainda não têm guardas
                int availableCount = 0;
                for (String v : r.vertices) {
                    if (!guards.contains(v)) {
                        availableCount++;
                    }
                }

                // Queremos o retângulo com MENOS opções de vértices livres
                if (availableCount < minAvailableVertices) {
                    minAvailableVertices = availableCount;
                    rarestRectangle = r;
                }
            }

            // 2. ESCOLHA NÃO-GULOSA: Pegar o primeiro vértice livre que encontrar no retângulo crítico
            String chosenVertex = null;
            for (String v : rarestRectangle.vertices) {
                if (!guards.contains(v)) {
                    chosenVertex = v;
                    break; // Pegou o primeiro? Para a busca.
                }
            }

            // Se por algum motivo todos os vértices já tinham guardas (mas o retângulo não estava marcado),
            // pega o primeiro do vértice do retângulo apenas para fechar a lógica.
            if (chosenVertex == null) {
                chosenVertex = rarestRectangle.vertices.get(0);
            }

            // Coloca o guarda
            guards.add(chosenVertex);

            // Atualiza o status de cobertura de todos os retângulos afetados
            int newlyCoveredCount = 0;
            for (Rectangle r : rects) {
                if (!covered.contains(r.id) && r.vertices.contains(chosenVertex)) {
                    covered.add(r.id);
                    newlyCoveredCount++;
                }
            }

            System.out.println("First-Fail target selected. Guard placed at: " + chosenVertex + 
                               " | Covered " + newlyCoveredCount + " new rectangle(s) por tabela.");
        }

        System.out.println();
        System.out.println("FINAL SOLUTION (FIRST-FAIL ONLY)");
        System.out.println("--------------------------------");
        System.out.println("Guards used: " + guards.size());
        System.out.println("Vertices: " + guards);
    }
}