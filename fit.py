#!/usr/bin/env python2

import argparse,os
import sys
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument('--o',action='store', type=str, default = "diffNuisances.root")
parser.add_argument('--M',action='store', type=str, default = "FitDiagnostics")
parser.add_argument('--t',action='store', type=str, default = "-1")
parser.add_argument('--freeze',action='store', type=str, default = "r")
parser.add_argument('--set',action='store', type=str, default = "r=1")
parser.add_argument('--poi',action='store', type=str, default = "yt")
parser.add_argument('--opt',action='store', type=str, default = "--robustFit=1 --do95=1 --cminPreScan")

args = parser.parse_args()

cmssw = os.environ['CMSSW_BASE']
if "CMSSW_8_1_" not in cmssw:
	print 'ENV NOT LOADED'
	

command1 = 'combine -M '+args.M+' -d card.root --redefineSignalPOIs '+args.poi+' --freezeParameters '+args.freeze+' --setParameters '+args.set+' -t '+args.t+' '+args.opt

print 'running combine:',command1
os.system(command1)

command2 = 'python ../../diffNuisances.py --poi '+args.poi+' -a fitDiagnostics.root -g '+args.o
print 'running diffNuisances:',command2
os.system(command2)
