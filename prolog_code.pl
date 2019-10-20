countDiseases(X,Y):- length(X,Y).
noCriticalDisease(X):- not(member(hearing,X)).
mentalHealth(X):- member(mental,X).


risk(Age,low,Diseases,Reduce):- reduce(Reduce), risk(Age,medium,Diseases,_),!.

risk(Age,low,Diseases,_) :- age(Age,X), X=acceptable, countDiseases(Diseases,Y), Y<2,
    						noCriticalDisease(Diseases), not(mentalHealth(Diseases)),!.

risk(Age,medium,Diseases,_):-  noCriticalDisease(Diseases), (   
                                                            (mentalHealth(Diseases), age(Age,X), X = over55,!); 
    						  								(not(mentalHealth(Diseases)), countDiseases(Diseases,Y), Y=2,!)).
    						 

risk(Age,high,Diseases,_):-(    member(hearing,Diseases);(countDiseases(Diseases,X), X>2));
    						(   mentalHealth(Diseases), age(Age,X), X = over65).

risk(Age,rejected,Diseases,_):- risk(Age,high,Diseases,_),!.

age(Age, over55):- Age>54, Age<65.
age(Age, acceptable):- Age>20,Age<70.
age(Age, over65):- Age>64, Age<70.


country(switzerland).
reduce(yes).

findRisk(Age,Risk,Diseases,Country,Reduce):- risk(Age,Risk, Diseases,Reduce), country(Country).

