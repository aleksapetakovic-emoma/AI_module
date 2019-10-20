countDiseases(X,Y):- length(X,Y).
criticalDisease(X,Y):- not(member(X,Y)).
mentalHealth(X):- member(mental,X).

risk(_,high,Diseases):- member(hearing,Diseases),!.
risk(Age,low,Diseases) :- age(Age,X), X=below55, countDiseases(Diseases,Y), Y<2,criticalDisease(hearing,Diseases).
risk(_,low,Diseases):- countDiseases(Diseases,X), X<2, not(member(mental,Diseases)), criticalDisease(hearing,Diseases).
risk(Age,medium,Diseases):- mentalHealth(Disease), age(Age,X), X = over55, countDiseases(Diseases,Y), Y<2,  criticalDisease(hearing,Diseases).
risk(_,medium,Diseases):- countDiseases(Diseases,Y), Y<3, Y>1, criticalDisease(hearing,Diseases).
risk(_,high,Diseases):- countDiseases(Diseases,X), X>2.
risk(Age,high,Diseases):- member(mental,Diseases), age(Age,X), X = over65.

risk(Age,low,Diseases,Reduce):- reduce(Reduce,yes), risk(Age,medium,Diseases),!.
risk(Age,low,Diseases,Reduce):- reduce(Reduce,no), risk(Age,low,Diseases),!.

risk(Age,low,Diseases,_):- risk(Age,low,Diseases),!.
risk(Age,medium,Diseases,Reduce):- reduce(Reduce,no), risk(Age,medium,Diseases),!.
risk(Age,high,Diseases,_):-  risk(Age,high,Diseases).
risk(Age,rejected,Diseases,_):- risk(Age,high,Diseases),!.

age(Age, over55):- Age>54, Age<65, age(over55).
age(Age, below55):- Age>20,Age<55,  age(below55).
age(Age, over65):- Age>64, Age<70, age(over65).

age(below55).
age(over55).
age(over65).

country(switzerland).

reduce(Reduce, yes):- Reduce = yes.
reduce(Reduce, no):- Reduce = no.

findRisk(Age,Risk,Diseases,Country,Reduce):- risk(Age,Risk, Diseases,Reduce), country(Country).

