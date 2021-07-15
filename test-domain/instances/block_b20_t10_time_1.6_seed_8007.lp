#const horizon=32.

block(1..20).
loc(table).
loc(B) :- block(B).

init(on(7,table)).
init(on(8,table)).
init(on(19,8)).
init(on(16,19)).
init(on(3,table)).
init(on(2,table)).
init(on(18,table)).
init(on(11,table)).
init(on(6,11)).
init(on(15,table)).
init(on(20,15)).
init(on(5,table)).
init(on(17,table)).
init(on(1,17)).
init(on(12,1)).
init(on(4,table)).
init(on(9,table)).
init(on(13,table)).
init(on(14,table)).
init(on(10,14)).

goal(on(20,table)).
goal(on(1,20)).
goal(on(11,1)).
goal(on(2,11)).

goal(on(12,table)).

goal(on(10,table)).
goal(on(8,10)).

goal(on(7,table)).

goal(on(18,table)).
goal(on(15,18)).

goal(on(14,table)).

goal(on(13,table)).
goal(on(17,13)).
goal(on(9,17)).
goal(on(4,9)).

goal(on(16,table)).
goal(on(3,16)).

goal(on(5,table)).
goal(on(6,5)).

goal(on(19,table)).
