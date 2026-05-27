package com.example;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import com.google.ortools.Loader;
import com.google.ortools.sat.CpModel;
import com.google.ortools.sat.CpSolver;
import com.google.ortools.sat.CpSolverStatus;
import com.google.ortools.sat.IntVar;
import com.google.ortools.sat.LinearExpr;

public class OrToolsSolution {

    // Classe para representar nossos retângulos no formato do seu mapa
    static class Rectangle {
        int id;
        List<String> vertices;

        Rectangle(int id, String... v) {
            this.id = id;
            this.vertices = Arrays.asList(v);
        }
    }

    public static void main(String[] args) {
        // Inicializa as bibliotecas nativas do OR-Tools
        Loader.loadNativeLibraries();

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

        // Coleta todos os vértices únicos do mapa
        Set<String> allVertices = new TreeSet<>();
        for (Rectangle r : rects) {
            allVertices.addAll(r.vertices);
        }

        // Cria o modelo do CP-SAT
        CpModel model = new CpModel();

        // Dicionário ajustado para usar IntVar, evitando erros de atribuição de tipos no Java
        Map<String, IntVar> vertexVars = new HashMap<>();
        List<IntVar> totalGuardsList = new ArrayList<>();

        // Cria uma variável binária para cada letra (0 se não tem guarda, 1 se tem)
        for (String vertex : allVertices) {
            IntVar var = model.newBoolVar(vertex);
            vertexVars.put(vertex, var);
            totalGuardsList.add(var);
        }

        // RESTRIÇÃO: Cada retângulo deve ter PELO MENOS 1 vértice ativado (com guarda)
        for (Rectangle r : rects) {
            List<IntVar> rectVariables = new ArrayList<>(); // Alterado para IntVar
            for (String v : r.vertices) {
                rectVariables.add(vertexVars.get(v));
            }
            // Soma(vértices do retângulo) >= 1
            model.addGreaterOrEqual(LinearExpr.sum(rectVariables.toArray(new IntVar[0])), 1);
        }

        // FUNÇÃO OBJETIVO: Minimizar o número total de guardas no mapa
        LinearExpr totalGuards = LinearExpr.sum(totalGuardsList.toArray(new IntVar[0]));
        model.minimize(totalGuards);

        // Cria o Solver e resolve o problema
        CpSolver solver = new CpSolver();
        CpSolverStatus status = solver.solve(model);

        // Exibe os resultados obtidos
        System.out.println("STATUS DO SOLVER: " + status);
        if (status == CpSolverStatus.OPTIMAL || status == CpSolverStatus.FEASIBLE) {
            System.out.println();
            System.out.println("SOLUÇÃO ÓTIMA ENCONTRADA");
            System.out.println("-------------------------");
            System.out.println("Total mínimo de guardas: " + (int) solver.objectiveValue());
            
            List<String> chosenVertices = new ArrayList<>();
            for (String vertex : allVertices) {
                if (solver.value(vertexVars.get(vertex)) == 1) {
                    chosenVertices.add(vertex);
                }
            }
            System.out.println("Posições dos guardas: " + chosenVertices);
        } else {
            System.out.println("Não foi possível encontrar uma solução válida.");
        }
    }
}