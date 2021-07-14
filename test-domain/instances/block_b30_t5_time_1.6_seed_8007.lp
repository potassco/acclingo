#const horizon=48.

block(1..30).
loc(table).
loc(B) :- block(B).

init(on(4,table)).
init(on(18,table)).
init(on(10,table)).
init(on(25,10)).
init(on(11,table)).
init(on(23,11)).
init(on(16,23)).
init(on(19,table)).
init(on(3,19)).
init(on(17,table)).
init(on(21,table)).
init(on(12,21)).
init(on(28,table)).
init(on(15,table)).
init(on(20,table)).
init(on(2,table)).
init(on(13,table)).
init(on(1,table)).
init(on(24,1)).
init(on(6,table)).
init(on(26,6)).
init(on(22,table)).
init(on(7,table)).
init(on(29,7)).
init(on(14,table)).
init(on(8,table)).
init(on(27,table)).
init(on(9,27)).
init(on(5,table)).
init(on(30,table)).

goal(on(8,table)).
goal(on(23,8)).
goal(on(25,23)).
goal(on(13,25)).
goal(on(3,13)).
goal(on(26,3)).

goal(on(7,table)).
goal(on(4,7)).
goal(on(2,4)).
goal(on(28,2)).
goal(on(20,28)).
goal(on(11,20)).
goal(on(5,11)).
goal(on(24,5)).

goal(on(19,table)).
goal(on(15,19)).
goal(on(22,15)).
goal(on(18,22)).

goal(on(16,table)).
goal(on(17,16)).
goal(on(1,17)).
goal(on(14,1)).
goal(on(12,14)).
goal(on(10,12)).

goal(on(21,table)).
goal(on(9,21)).
goal(on(27,9)).
goal(on(30,27)).
goal(on(29,30)).
goal(on(6,29)).
