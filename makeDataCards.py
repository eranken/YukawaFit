from Framework.Core import *
import argparse,os

#set options

parser = argparse.ArgumentParser()
parser.add_argument('--input',action='store')
parser.add_argument('--year', action='store', type=str, default='2017')
parser.add_argument('--chan', action='store', type=str, default='all')

option = parser.parse_args()

inDir = 'Input/'+option.input+'/'
outDir = 'Cards/'+option.input+'/'
print 'Input Directory: ',inDir
print 'Output Directory: ',outDir
print '--------'
year = option.year
chan = option.chan

#load systematic list
sysfile = open(inDir+'combine_sys_'+year+chan+'.txt')
syslist = sysfile.read().split('\n')
syslist = filter(None, syslist) #

#lumi uncertainty
shortyear = year[2:]
if shortyear == '17':
	lumiunc =0.023
else:
	lumiunc = 0.025
lumiunc+=1.

#define processes
process = [
		"vj",
		"ttsig",
		"st",
		]

#add normalization systematics
print 'defining lnN uncs'
systematics = [
		lnNSystematic("lumi_"+shortyear	,["ttsig","vj","st"]	,[lumiunc,lumiunc,lumiunc]),
		lnNSystematic("vj_norm"	,["vj"]	,[1.15]),
		lnNSystematic("tt_norm"	,["ttsig"]	,[1.1]),
		lnNSystematic("st_norm"	,["st"]	,[1.15])
		]

#add shape systematics
print 'loading shapes: '
for sys in syslist:
	print sys
	systematics.append(ShapeSystematic(sys,["ttsig"]))

print "--------"
rootFileReader = RootFileReader()
rootFileReader.readFile(inDir+'combine_'+year+chan+'.root')
binCollection = rootFileReader.createBinCollection(process,systematics)

#load EW corrections
textFilePath = inDir+'combine_EW_'+year+chan+'.txt'
textFileReader = TextFileReader()
textFileReader.readTextFile(textFilePath,binCollection)

#make the cards
if not os.path.exists(outDir):
	os.makedirs(outDir)

for ibin,anaBin in binCollection.iteritems():
	dataCard = DataCard(anaBin)
	dataCard.makeCard(outDir,year,chan)
	dataCard.makeRootFile(outDir,year,chan)
	print "made bin ",ibin
rootFileReader.cleanUp()
