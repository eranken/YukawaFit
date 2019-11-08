import argparse,os
import sys


parser = argparse.ArgumentParser()
parser.add_argument('--o',action='store', type=str, default = "impacts")
parser.add_argument('--M',action='store', type=str, default = "MaxLikelihoodFit")
parser.add_argument('--t',action='store', type=str, default = "-1")
parser.add_argument('--freeze',action='store', type=str, default = "r")
parser.add_argument('--set',action='store', type=str, default = "r=1")
parser.add_argument('--poi',action='store', type=str, default = "yt")

args = parser.parse_args()

command1= 'combineTool.py -M Impacts -d card.root -m 125 --redefineSignalPOIs '+args.poi+' --freezeParameters '+args.freeze+' --setParameters '+args.set+' --doInitialFit --robustFit 1 -t '+args.t
print "1st Step: ", command1
os.system(command1)

command2= 'combineTool.py -M Impacts -d card.root -m 125 --redefineSignalPOIs '+args.poi+' --freezeParameters '+args.freeze+' --setParameters '+args.set+' --doFits --robustFit 1 -t '+args.t+' --cminPreScan'
print "2nd Step: ", command2
os.system(command2)

command3='combineTool.py -M Impacts -d card.root -m 125 --redefineSignalPOIs '+args.poi+' --freezeParameters '+args.freeze+' --setParameters '+args.set+' -o'+args.o+'.json'
print "3rd Step (json): ",command3
os.system(command3)

command4='plotImpacts.py -i '+args.o+'.json -o '+args.o
print "Final step, making pdf: ",command4
os.system(command4)

