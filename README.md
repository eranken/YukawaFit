# YukawaFit
# using combine to fit yukawa coupling

Sample input files are provided in "Input/test/"
To make datacards out of these, run

> python makeDataCards.py --input test --year 2017 --chan all

Datacards will be stored in "Cards/test/"
To prepare for fitting:

> cd DataCards/test
> combineCards.py bin*.txt > card.txt
> text2workspace.py card.txt

Two fitting scripts are included, which should be run from this datacard dir. they are targetting the resulting file "card.root" :

> python ../../fit.py

and

> python ../../impacts.py 
