:- use_module(library(clpfd)).
:- use_module(library(lists)).

retangulo(r1,  [1]).
retangulo(r2,  [1,3,2]).
retangulo(r3,  [5,6]).
retangulo(r4,  [5,4,3,2]).
retangulo(r5,  [2,1]).
retangulo(r6,  [3,4]).
retangulo(r7,  [7,6,8]).
retangulo(r8,  [7,6,4,5]).
retangulo(r9,  [8,7]).
retangulo(r10, [8]).


% Converter índices em variáveis

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

resolver(Vars, Total) :-
    statistics(cputime, T0),
    % 10 vértices
    length(Vars, 10),

    % variáveis binárias
    Vars ins 0..1,

    Retangulos = [r1,r2,r3,r4,r5,r6,r7,r8,r9,r10],
    todos_cobertos(Retangulos, Vars),

    % minimizar quantidade de guardas
    sum(Vars, #=, Total),

    labeling([min(Total)], Vars),
    statistics(cputime, T1),
    T is T1 - T0,
    format('CPU time: ~w~n', [T]).
    
