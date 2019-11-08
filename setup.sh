THISDIR=`pwd`
CMSSW_LOC=$SPACE
export SCRAM_ARCH=slc6_amd64_gcc700
cd $CMSSW_LOC/CMSSW_10_2_18
eval `scramv1 runtime -sh`
cd $THISDIR
