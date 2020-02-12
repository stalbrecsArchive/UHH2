# This is a small example how the crab api can easily be used to create something like multi crab.
# It has some additional features like also creating the xml files for you.
# For it to work you need inputDatasets & requestNames apart from the classical part
#
# Make sure to have a unique directory where your joboutput is saved, otherwise the script gets confused and you too!!
#
# Usage ./CrabConfig ConfigFile [options]
#
# Take care here to make the request names *nice*
#
# autocomplete_Datasets(ListOfDatasets) works also for several entries with *

import sys,os
sys.path.append('.')
import re
from DasQuery import autocomplete_Datasets


def get_request_name(dataset_name):
    """Generate short string to use for request name from full dataset name"""
    modified_name = dataset_name.split('/')[1]
    modified_name = modified_name.replace('_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', '_P8M1')
    modified_name = modified_name.replace('_TuneCP5_13TeV-madgraphMLM-pythia8', '_CP5')
    modified_name = modified_name.replace('_TuneCUETP8M1_13TeV_pythia8', '_P8M1')

    # request name can only be 100 characters maximum
    # at this point we need to chop it down, to allow for campaign, time, date, ext2, v2
    max_len = 100-34
    if len(modified_name) > max_len:
        modified_name = modified_name[:max_len]

    # Add run year+period for data
    year_match = re.search(r'201[678][A-Z]', dataset_name)
    if year_match:
        modified_name += '_'
        modified_name += year_match.group(0)

    # Add MC campaign
    if "Summer16" in dataset_name:
        modified_name += "_Summer16"
    elif "Fall17" in dataset_name:
        modified_name += "_Fall17"
    elif "Autumn18" in dataset_name:
        modified_name += "_Autumn18"

    if 'ext1' in dataset_name:
        modified_name += '_ext1'
    elif 'ext2' in dataset_name:
        modified_name += '_ext2'
    elif 'ext' in dataset_name:
        modified_name += '_ext'

    # For e.g. Run2016B which is split into 2
    if "ver1" in dataset_name:
        modified_name += "_ver1"
    elif "ver2" in dataset_name:
        modified_name += "_ver2"

    if "-v1" in dataset_name:
        modified_name += "_v1"
    elif "-v2" in dataset_name:
        modified_name += "_v2"

    return modified_name



# inputDatasets = ['/JetHT/Run2016*-17Jul2018*/MINIAOD']
inputDatasets = [ #'/SingleElectron/Run2017C-31Mar2018-v1/MINIAOD',
                  '/SingleElectron/Run2017F-31Mar2018-v1/MINIAOD'
]
# inputDatasets = ['/JetHT/Run2016H-17Jul2018-v1/MINIAOD']
inputDatasets = autocomplete_Datasets(inputDatasets)
requestNames = [get_request_name(x) for x in inputDatasets]

# ===============================================================================
# Classical part of crab, after resolving the * it uses in the example below just the first entry
#

from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.ClientExceptions import ProxyException
import os
import re


config = config()
config.General.workArea = 'ul17_crab'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = os.path.join(os.environ['CMSSW_BASE'], 'src/UHH2/core/python/ntuplewriter_data_2017v2.py')
config.JobType.outputFiles = ["Ntuple.root"]
config.JobType.maxMemoryMB = 2500

import FWCore.PythonUtilities.LumiList as LumiList
RunC=[299481,299480,299479,299478,299477,299593,299594,299595,299597]
RunF= [306459,306456,305064,306125]
LumiList.LumiList(runs=RunC+RunF).writeJSON(fileName='UL2017_RunCF_lumi_mask.json')
config.Data.lumiMask='UL2017_RunCF_lumi_mask.json'

config.Data.inputDBS = 'global'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 24000
# config.Data.splitting = 'FileBased'
# config.Data.unitsPerJob = 1
# config.JobType.maxJobRuntimeMin = 2927
try:
    # Add subdirectory using year from config filename
    pset = os.path.basename(config.JobType.psetName)
    result = re.search(r'201[\d](v\d)?', pset)
    if not result:
        raise RuntimeError("Cannot extract year from psetName! Does your psetName have 201* in it?")
    year = result.group()
    config.Data.outLFNDirBase = '/store/user/%s/RunII_102X_v1/%s/' % (getUsernameFromSiteDB(), year)
except ProxyException as e:
    print "Encountered ProxyException:"
    print e.message
    print "Not setting config.Data.outLFNDirBase, will use default"

config.Data.publication = False
config.JobType.sendExternalFolder = True
#config.Data.allowNonValidInputDataset = True
#config.Data.publishDataName = 'CRAB3_tutorial_May2015_MC_analysis'

config.Site.storageSite = 'T2_DE_DESY'

if len(inputDatasets) > 0 and len(requestNames) > 0:
    config.General.requestName = requestNames[0]
    config.Data.inputDataset = inputDatasets[0]


