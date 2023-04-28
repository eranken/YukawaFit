THISDIR=`pwd`
#put your cmssw base directory here
CMSSW_LOC=$CMS
export SCRAM_ARCH=slc6_amd64_gcc700
cd $CMSSW_LOC/CMSSW_10_2_13
eval `scramv1 runtime -sh`
cd $THISDIR
