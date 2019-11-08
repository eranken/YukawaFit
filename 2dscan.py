import argparse,os
import sys
from subprocess import call

#comment

parser = argparse.ArgumentParser()
parser.add_argument('--t',action='store', type=str, default = "-1")
parser.add_argument('--width',action='store', type=str, default = "2.5")
parser.add_argument('--freeze',action='store', type=str, default = "")
parser.add_argument('--pts',action='store', type=str, default = "2500")
parser.add_argument('--set',action='store', type=str, default = "")
parser.add_argument('--poi',action='store', type=str, default = "")
parser.add_argument('--opt',action='store', type=str, default = "")
parser.add_argument('--P',action='store', type=str, default = "yt")
parser.add_argument('--ytpos',dest='ytpos', action='store_true')
parser.add_argument('--out',action='store', type=str, default = "2dscan")
parser.set_defaults(ytpos=False)

(args, opts) = parser.parse_known_args()
width = args.width
params = args.P.split(',')

# default vals
ytmax = '10'
ytmin = '-10'

# overwrite defaults if scanning yt
if 'yt' in params:
	ytmin = '-'+width
	ytmax = width

# finally, overwrite minimum if constraining yt > 0 is desired
if args.ytpos:
	ytmin = '0'


mystr = 'combine -M MultiDimFit -d card.root --algo=grid --points='+args.pts
mystr += ' --redefineSignalPOIs yt,'
for param in params:
	if param != 'yt':
		mystr += param+','
mystr += ' --freezeParameters r,'+args.freeze
mystr += ' --setParameters r=1,'+args.set
mystr += ' -t '+args.t
for param in params:
	mystr += ' -P '+param
mystr += ' --setParameterRanges yt='+ytmin+','+ytmax+':'
for param in params:
	if param !='yt':
		mystr+= param+'=-'+width+','+width+':'
mystr += ' --saveInactivePOI 1 --floatOtherPOIs=1'
for opt in opts:
	mystr += ' '+opt

print mystr
os.system(mystr)

outfile = args.out
for param in params:
	outfile+="_"+param
outfile+='.root'
print 'mv higgsCombineTest.MultiDimFit.mH120.root '+outfile
os.system('mv higgsCombineTest.MultiDimFit.mH120.root '+outfile)
