THISDIR=`pwd`
CMSSW_LOC=$SPACE
export SCRAM_ARCH=slc6_amd64_gcc530
cd $CMSSW_LOC/CMSSW_8_1_0
eval `scramv1 runtime -sh`
cd $THISDIR
