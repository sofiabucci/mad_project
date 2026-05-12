from itertools import combinations


def check_solution(selection):
    x = {i: 1 if i in selection else 0 for i in range(1, 9)}
    return (
        x[8] >= 1 and
        x[8] + x[7] >= 1 and
        x[7] + x[6] + x[4] + x[5] >= 1 and
        x[7] + x[6] + x[8] >= 1 and
        x[3] + x[4] >= 1 and
        x[2] + x[1] >= 1 and
        x[5] + x[4] + x[3] + x[2] >= 1 and
        x[5] + x[6] >= 1 and
        x[1] + x[3] + x[2] >= 1 and
        x[1] >= 1
    )


def solve_partRects_bruteforce():
    best_cost = None
    best_solutions = []

    for k in range(1, 9):
        for combo in combinations(range(1, 9), k):
            if check_solution(combo):
                best_cost = k
                best_solutions.append(combo)
        if best_cost is not None:
            break

    if best_cost is None:
        print("No feasible solution found.")
        return

    print("Optimal cost:", best_cost)
    print("Optimal guard placements:")
    for sol in best_solutions:
        print(" ", sol)


def solve_partRects():
    try:
        from ortools.linear_solver import pywraplp
    except ImportError:
        print("OR-Tools não encontrado. Usando busca por força bruta.")
        solve_partRects_bruteforce()
        return

    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        print("Solver SCIP não disponível no OR-Tools. Usando busca por força bruta.")
        solve_partRects_bruteforce()
        return

    x = {i: solver.IntVar(0, 1, f'x_{i}') for i in range(1, 9)}

    solver.Add(x[8] >= 1)
    solver.Add(x[8] + x[7] >= 1)
    solver.Add(x[7] + x[6] + x[4] + x[5] >= 1)
    solver.Add(x[7] + x[6] + x[8] >= 1)
    solver.Add(x[3] + x[4] >= 1)
    solver.Add(x[2] + x[1] >= 1)
    solver.Add(x[5] + x[4] + x[3] + x[2] >= 1)
    solver.Add(x[5] + x[6] >= 1)
    solver.Add(x[1] + x[3] + x[2] >= 1)
    solver.Add(x[1] >= 1)

    objective = solver.Objective()
    for i in range(1, 9):
        objective.SetCoefficient(x[i], 1)
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal cost:", objective.Value())
        print("Optimal guard placements:")
        solution = [i for i in range(1, 9) if x[i].solution_value() > 0.5]
        print(" ", solution)
    else:
        print("No optimal solution found. Fallback para força bruta.")
        solve_partRects_bruteforce()


if __name__ == '__main__':
    solve_partRects()
