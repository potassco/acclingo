#const horizon=32.

block(1..20).
loc(table).
loc(B) :- block(B).

init(on(4,table)).
init(on(5,4)).
init(on(1,5)).
init(on(9,table)).
init(on(16,table)).
init(on(12,table)).
init(on(7,table)).
init(on(17,7)).
init(on(15,table)).
init(on(18,15)).
init(on(3,table)).
init(on(10,table)).
init(on(19,table)).
init(on(13,19)).
init(on(6,table)).
init(on(8,6)).
init(on(2,table)).
init(on(11,table)).
init(on(14,table)).
init(on(20,14)).

goal(on(18,table)).
goal(on(13,18)).
goal(on(6,13)).
goal(on(9,6)).

goal(on(1,table)).
goal(on(5,1)).
goal(on(8,5)).
goal(on(10,8)).
goal(on(12,10)).

goal(on(19,table)).
goal(on(14,19)).
goal(on(11,14)).
goal(on(17,11)).

goal(on(7,table)).
goal(on(3,7)).
goal(on(2,3)).

goal(on(15,table)).
goal(on(20,15)).
goal(on(16,20)).
goal(on(4,16)).
