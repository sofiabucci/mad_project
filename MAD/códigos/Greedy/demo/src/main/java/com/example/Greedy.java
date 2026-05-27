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

public class Greedy {

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

        // Retângulos da figura
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

        // Retângulos ainda não cobertos
        Set<Integer> covered = new HashSet<>();

        // Guardas escolhidos
        Set<String> guards = new LinkedHashSet<>();

        /*
            GREEDY PRINCIPAL

            Em cada passo:
            1. Escolher o vértice que cobre MAIS
               retângulos ainda não cobertos.
        */

        while (covered.size() < rects.size()) {

            String bestVertex = null;
            int bestCoverage = -1;

            // Descobrir todos os vértices existentes
            Set<String> allVertices = new HashSet<>();

            for (Rectangle r : rects) {
                allVertices.addAll(r.vertices);
            }

            // Testar cada vértice
            for (String vertex : allVertices) {

                // Ignorar vértices já usados
                if (guards.contains(vertex))
                    continue;

                int coverage = 0;

                // Contar quantos retângulos ainda não cobertos
                // este vértice consegue cobrir
                for (Rectangle r : rects) {

                    if (!covered.contains(r.id) &&
                        r.vertices.contains(vertex)) {

                        coverage++;
                    }
                }

                // Atualizar melhor vértice
                if (coverage > bestCoverage) {
                    bestCoverage = coverage;
                    bestVertex = vertex;
                }
            }

            // Adicionar guarda
            guards.add(bestVertex);

            // Marcar retângulos cobertos
            for (Rectangle r : rects) {

                if (r.vertices.contains(bestVertex)) {
                    covered.add(r.id);
                }
            }

            System.out.println(
                "Guard placed at vertex: " +
                bestVertex +
                " | Covers " +
                bestCoverage +
                " rectangle(s)"
            );
        }

        System.out.println();
        System.out.println("FINAL SOLUTION");
        System.out.println("---------------");
        System.out.println("Guards used: " + guards.size());
        System.out.println("Vertices: " + guards);
    }
}