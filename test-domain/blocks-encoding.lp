
time(0..horizon).

action(move(B,L)) :- block(B), loc(L), B != L.


on(B,B2,0) :- init(on(B,B2)).


{do(A,T) : action(A)} 1 :- time(T), T>0.
1 {on(B,L,T) : loc(L)} 1 :- block(B), time(T), T>0.

clear(B,T) :- not on(B2,B,T) : block(B2), B2 != B; block(B), time(T).
clear(table,T) :- time(T).

%precondition
:- do(move(B,L),T), not clear(L,T-1).
:- do(move(B,L),T), not clear(B,T-1).

%postcodition
:- do(move(B,L),T), not on(B,L,T).
%on(B,L,T) :- do(move(B,L),T).

%inertia
:- on(B,L,T), not on(B,L,T-1), not do(move(B,L),T), block(B), time(T), T>0.

% cant have 2 blocks on 1 block
:- on(B1,B,T), on(B2,B,T), B1 < B2, block(B).

% cant have 1 block on 2 blocks
:- on(B,B1,T), on(B,B2,T), B1 < B2.

% block can't be on top of each other
:- on(B1,B2,T), on(B2,B1,T).

% block can't be on itself
:- on(B,B,T), time(T).

:- not on(B,L,horizon), goal(on(B,L)).
