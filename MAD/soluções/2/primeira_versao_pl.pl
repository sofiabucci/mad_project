:- use_module(library(clpfd)).


/*retangulo(r1,  [1]).
retangulo(r2,  [1,3,2]).
retangulo(r3,  [5,6]).
retangulo(r4,  [5,4,3,2]).
retangulo(r5,  [2,1]).
retangulo(r6,  [3,4]).
retangulo(r7,  [7,6,8]).
retangulo(r8,  [7,6,4,5]).
retangulo(r9,  [8,7]).
retangulo(r10, [8]).
retangulo(r11,  [1,15]).
retangulo(r12,  [12,13]).
retangulo(r13,  [13,15]).
retangulo(r14,  [15,14,13,12]).
retangulo(r15,  [12,11]).
retangulo(r16,  [13,14,16]).
retangulo(r17,  [16,18]).
retangulo(r18,  [17,16,14,15]).
retangulo(r19,  [18,17]).
retangulo(r20, [18]).*/

vertices_vars([], _, []).

vertices_vars([I|Is], Vars, [X|Xs]) :-
    nth1(I, Vars, X),
    vertices_vars(Is, Vars, Xs).

coberto(Vertices, Vars) :-
    vertices_vars(Vertices, Vars, VarsRet),
    sum(VarsRet, #>=, 1).

todos_cobertos([], _).

todos_cobertos([R|Rs], Vars) :-
    retangulo(R, Vertices),
    coberto(Vertices, Vars),
    todos_cobertos(Rs, Vars).

num_verts(N) :-
    findall(Vs, retangulo(_,Vs), Lista),
    append(Lista, Todos),
    max_list(Todos, N).

resolver(Vars, Total) :-
    statistics(cputime, T0),
    num_verts(N),
    length(Vars, N),
    Vars ins 0..1,
    findall(R, retangulo(R,_), Retangulos),
    todos_cobertos(Retangulos, Vars),
    sum(Vars, #=, Total),
    Total #>= 1,
    labeling([min(Total)], Vars),%adicionado first fail pra ver se melhora performance
    statistics(cputime, T1),
    T is T1 - T0,
    format('CPU time: ~w~n', [T]).

output(Vars, Total) :-
    % recolhe todos os pares Total-Solucao
    findall(Total-Vars, resolver(Vars, Total), Solucoes),

    % determina o valor minimo
    pairs_keys(Solucoes, Totais),
    min_list(Totais, TotalMin),

    % filtra apenas as solucoes com esse valor
    include([T-_]>>(T =:= TotalMin), Solucoes, Otimas),
    length(Otimas, L),

    format('Valor otimo: ~w~n', [TotalMin]),
    format('~w solucao(oes) otima(s) encontrada(s)~n~n', [L]),

    % imprime cada solucao otima
    forall(
        member(_-S, Otimas),
        (format('Solucao: ~w~n', [S]))
    ).