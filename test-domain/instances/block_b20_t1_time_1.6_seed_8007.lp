#const horizon=32.

block(1..20).
loc(table).
loc(B) :- block(B).

init(on(2,table)).
init(on(8,table)).
init(on(13,8)).
init(on(20,table)).
init(on(18,20)).
init(on(6,table)).
init(on(10,table)).
init(on(14,10)).
init(on(12,table)).
init(on(4,table)).
init(on(17,4)).
init(on(15,table)).
init(on(5,table)).
init(on(7,table)).
init(on(1,7)).
init(on(11,table)).
init(on(16,11)).
init(on(19,16)).
init(on(9,19)).
init(on(3,table)).

goal(on(3,table)).
goal(on(5,3)).
goal(on(13,5)).
goal(on(2,13)).
goal(on(7,2)).
goal(on(14,7)).
goal(on(9,14)).
goal(on(19,9)).
goal(on(17,19)).
goal(on(20,17)).
goal(on(11,20)).
goal(on(16,11)).
goal(on(4,16)).
goal(on(10,4)).
goal(on(15,10)).
goal(on(8,15)).
goal(on(6,8)).
goal(on(18,6)).
goal(on(1,18)).
goal(on(12,1)).
