#const horizon=48.

block(1..30).
loc(table).
loc(B) :- block(B).

init(on(23,table)).
init(on(5,23)).
init(on(12,table)).
init(on(15,12)).
init(on(17,table)).
init(on(6,17)).
init(on(21,6)).
init(on(20,21)).
init(on(10,table)).
init(on(11,10)).
init(on(9,11)).
init(on(4,table)).
init(on(29,table)).
init(on(7,29)).
init(on(22,table)).
init(on(27,table)).
init(on(28,27)).
init(on(8,28)).
init(on(16,8)).
init(on(13,table)).
init(on(25,table)).
init(on(30,table)).
init(on(3,30)).
init(on(14,3)).
init(on(1,table)).
init(on(19,table)).
init(on(24,19)).
init(on(26,24)).
init(on(2,table)).
init(on(18,table)).

goal(on(16,table)).

goal(on(10,table)).
goal(on(28,10)).
goal(on(5,28)).
goal(on(20,5)).

goal(on(7,table)).
goal(on(1,7)).
goal(on(14,1)).
goal(on(13,14)).
goal(on(4,13)).

goal(on(9,table)).
goal(on(29,9)).

goal(on(23,table)).
goal(on(15,23)).
goal(on(18,15)).

goal(on(26,table)).
goal(on(8,26)).

goal(on(30,table)).
goal(on(21,30)).
goal(on(12,21)).

goal(on(27,table)).

goal(on(22,table)).
goal(on(24,22)).
goal(on(3,24)).
goal(on(25,3)).
goal(on(19,25)).

goal(on(6,table)).
goal(on(11,6)).
goal(on(2,11)).
goal(on(17,2)).
