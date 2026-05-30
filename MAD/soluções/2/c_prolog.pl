:- use_module(library(clpfd)).

% Factos da instância
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

% Código do c_prolog.pl
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

ordem_vars(Vars, VarsOrdenadas) :-
    length(Vars, N),
    numlist(1, N, Indices),
    findall(C-I,
        (member(I, Indices),
         findall(R, (retangulo(R,Vs), member(I,Vs)), Rs),
         length(Rs, C)),
        Pares),
    msort(Pares, Crescente),
    reverse(Crescente, Decrescente),
    pairs_values(Decrescente, IndicesOrdenados),
    maplist({Vars}/[I,V]>>(nth1(I, Vars, V)), IndicesOrdenados, VarsOrdenadas).

resolver_min(Vars, Total) :-
    statistics(cputime, T0),
    num_verts(N),
    length(Vars, N),
    Vars ins 0..1,
    findall(R, retangulo(R,_), Retangulos),
    todos_cobertos(Retangulos, Vars),
    sum(Vars, #=, Total),
    ordem_vars(Vars, VarsOrdenadas),
    labeling([min(Total)], VarsOrdenadas), !,
    statistics(cputime, T1),
    T is T1 - T0,
    format('CPU time (minimo): ~3f s~n', [T]).

resolver_fixado(Vars, Total) :-
    num_verts(N),
    length(Vars, N),
    Vars ins 0..1,
    findall(R, retangulo(R,_), Retangulos),
    todos_cobertos(Retangulos, Vars),
    sum(Vars, #=, Total),
    ordem_vars(Vars, VarsOrdenadas),
    labeling([], VarsOrdenadas).

output(Total) :-
    resolver_min(_Vars_min, Total),
    format('Valor otimo: ~w~n', [Total]),
    findall(Vars, resolver_fixado(Vars, Total), Solucoes),
    length(Solucoes, L),
    format('~w solucao(oes) otima(s)~n~n', [L]),
    forall(member(S, Solucoes), format('Solucao: ~w~n', [S])).