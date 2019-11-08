
import ROOT
from Systematic import *

class Process(object):
	def __init__(self,name,count):
		self.name = name
		self.count = count

class AnalysisBin(object):
	def __init__(self,binNumber):
		self.binNumber = binNumber
		self.processList = []
		self.systList = []

class TextFileReader(object):
	def readTextFile(self,filePath,binDict):
		textFile = open(filePath,"r")
		lines = textFile.readlines()
#read the yukawa bin rate coefficients. option to include uncertainty term as extra number in text file
		for line in lines:
			EWinfo = line.split()
			binNumber=EWinfo[0]
			c1=float(EWinfo[1])
			c2=float(EWinfo[2])
			c3=float(EWinfo[3])
			if len(EWinfo)==5:
				EWunc=float(EWinfo[4])
			else:
				EWunc=0.
			binDict[int(binNumber)].quadCoeff = [float(c1),float(c2),float(c3),float(EWunc)]

class RootFileReader(object):
	def __init__(self):
		self.bins = []

	def readFile(self,filePath):
		self.inputFile = ROOT.TFile(filePath,"READ")

	def cleanUp(self):
		self.inputFile.Close()

	def createBinCollection(self,process,systematics):
		objectNames = [ k.GetName() for k in self.inputFile.GetListOfKeys() ]
		dataHist = self.inputFile.Get("data_obs")
		nBins = dataHist.GetNbinsX()
		binDict = {}
		for ibin in range(1,nBins+1):
			binDict[ibin] = AnalysisBin(ibin)
		for ibin,anaBin in binDict.iteritems():
			processObj = Process("data",dataHist.GetBinContent(ibin))
			anaBin.data = processObj
			for eachprocess in process:
				hist = self.inputFile.Get(eachprocess)
				processObj = Process(eachprocess,hist.GetBinContent(ibin))
				anaBin.processList.append(processObj)
			for systematic in systematics:
				if systematic.systType == "shape":
					systematic.nBins = nBins
					for vary in ["Up","Down"]:
						hist = self.inputFile.Get(systematic.name+vary)
						systematic.binContent.update({str(ibin)+vary : hist.GetBinContent(ibin)})
#UNCOMMENT THIS TO PRINT BIN CONTENTS						
						#print str(ibin)+": "+str(vary)+": "+str(hist.GetBinContent(ibin))+" attributes:  "+str(systematic.name)+str(systematic.process)
				anaBin.systList.append(systematic)
		return binDict

class SystWriter(object):
	def makeMCSystLine(self,systematics,processList):
		outputStr = ""
		for systematic in systematics:
			if systematic.systType == "shape":
				outputStr += self.makeShapeLine(systematic,processList)
			elif systematic.systType == "lnN":
				outputStr += self.makelnNLine(systematic,processList)
		return outputStr

	@staticmethod
	def makelnNLine(systematic,processList):
		outputStr = ""
		outputStr += systematic.name+"\tlnN\t"
		correlationStr = ""
		for eachProcess in processList:
			if eachProcess.name not in systematic.process:
				correlationStr += "-\t"
			else:
				correlationStr += "%s\t"%systematic.systDict[eachProcess.name]
		outputStr += correlationStr
		outputStr +="\n"
		return outputStr

	@staticmethod
	def makeShapeLine(systematic,processList):
		outputStr = ""
		outputStr += systematic.getSystName()+"\tshape\t"
		correlationStr = ""
		for eachProcess in processList:
			if eachProcess.name not in systematic.process:
				correlationStr += "-\t"
			else:
				correlationStr += "1\t"
		outputStr += correlationStr
		outputStr +="\n"
		return outputStr

	def writeYukawa(self,binName,quadCoeff):
		outputStr = ""
		outputStr += "yt\tparam\t1.\t1.\t[0,10]\n"
		#outputStr += "yt\tflatParam\n"
#write the yukawa coupling quadratic bin rate formula
		ytLine = binName+"Rate\trateParam\tSignal\tttsig\t({0}*(@0)^2{1}*(@0){2})".format(
				quadCoeff[0],
				"+"+str(quadCoeff[1]) if quadCoeff[1] > 0. else "-"+str(abs(quadCoeff[1])),
				"+"+str(quadCoeff[2]) if quadCoeff[2] > 0. else "-"+str(abs(quadCoeff[2])),
				)
#optional EW uncertainty term
		if quadCoeff[3]!=0.:
			ytLine+="*(({0}*(@0)^2{1}*(@0){2}-1)*{3}+1)^(@1)\tyt,EWunc\n".format(
				quadCoeff[0],
				"+"+str(quadCoeff[1]) if quadCoeff[1] > 0. else "-"+str(abs(quadCoeff[1])),
				"+"+str(quadCoeff[2]) if quadCoeff[2] > 0. else "-"+str(abs(quadCoeff[2])),
				quadCoeff[3]
				)
		ytLine+=("\tyt" if quadCoeff[3]==0. else "\tyt,EWunc")
		ytLine+="\n"
		outputStr += ytLine
		#outputStr += binName+"Rate\trateParam\tSignal\tttsig\t{0}*(@0)^2\tyt\n".format(quadCoeff[0])
		outputStr += "\n"
		if quadCoeff[3]!=0.:
			outputStr += "EWunc\tparam\t0.\t1.\t[-5.,5.]"
		return outputStr

class DataCard(object):
	def __init__(self,analysisBin):
		self.analysisBin = analysisBin
		self.sep = "---------------------------------------------------------------------------------"
		self.makeStandardCardDetails()

	def makeHeader(self,rootFilePath):
		header = '''
*     number of categories
*     number of samples minus one
*     number of nuisance parameters
-----------------------------------------------------------------------
'''
		header += "shapes * * {0} $CHANNEL/$PROCESS $CHANNEL/$PROCESS_$SYSTEMATIC\n".format(rootFilePath.split("/")[-1])
		header += self.sep+"\n"
		header += "\n"
		return header

	def makeStandardCardDetails(self):
		self.rateParamLines = ""
		self.binName = "bin\t"
		self.processName = "process\t"
		self.processNum = "process\t"
		for iprocess,process in enumerate(self.analysisBin.processList):
			self.binName += "Signal\t"
			self.processName += process.name+"\t"
			if "ttsig" not in process.name:
				self.processNum += str(iprocess+1)+"\t"
			else:
				self.processNum += "0\t"
		self.binNameObservation = "bin\tSignal\t"
		self.observation = "observation"
		self.rates = "rate\t"
		self.sep = "---------------------------------------------------------------------------------"
		self.systLines = ""
		return

	def makeCard(self,outputDir,year,chan):
		outputStr = ""
		binName = "bin"+str(self.analysisBin.binNumber)+"_"+year+chan

		outputStr = self.makeHeader(outputDir+binName+".root")
		outputStr += self.binNameObservation+"\n"
		outputStr += self.observation+"\t"+str(self.analysisBin.data.count)+"\n"
		outputStr += self.sep+"\n"
		outputStr += self.binName+"\n"
		outputStr += "\n"
		outputStr += "\n"

		outputStr += self.processName+"\n"
		outputStr += self.processNum+"\n"

		outputStr += self.rates+"\t"
		for process in self.analysisBin.processList:
			outputStr += str(process.count)+"\t"
		outputStr += "\n"
		outputStr += self.sep+"\n"
		outputStr += "\n"

		systWriter = SystWriter()
		outputStr += systWriter.makeMCSystLine(self.analysisBin.systList,self.analysisBin.processList)
		outputStr += systWriter.writeYukawa(binName,self.analysisBin.quadCoeff)

		outputPath = outputDir+binName+".txt"

		outputFile = open(outputPath,"w")
		outputFile.write(outputStr)
		outputFile.close()

	def makeRootFile(self,outputDir,year,chan):
		iBin =self.analysisBin.binNumber
		binName = "bin"+str(self.analysisBin.binNumber)+"_"+year+chan
		outputFile = ROOT.TFile(outputDir+binName+".root","RECREATE")

		outputFile.mkdir("Signal")
		outputFile.cd("Signal")

		dataHist = ROOT.TH1D("data_obs","",1,-0.5,0.5)
		dataHist.SetBinContent(1,self.analysisBin.data.count)
		dataHist.Write()

		for process in self.analysisBin.processList:
			processHist = ROOT.TH1D(process.name,"",1,-0.5,0.5)
			processHist.SetBinContent(1,process.count)
			processHist.Write()

		for systematic in self.analysisBin.systList:
			if systematic.systType != "shape": continue
			for processName in systematic.process:
				for vary in ["Up","Down"]:
					tempHist = ROOT.TH1D(processName+"_"+systematic.name+vary,"",1,-0.5,0.5)
					tempHist.SetBinContent(1,systematic.binContent[str(iBin)+vary])
					tempHist.Write()
		outputFile.Close()
