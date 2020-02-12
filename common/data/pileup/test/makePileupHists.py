import os,json
import FWCore.PythonUtilities.LumiList as LumiList

def makePileupHist(myAnalysis,usedRuns):
    certJSON={
        '16':'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt',
        '17':'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt',
        '18':'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt',
    }

    year=''
    
    if('16' in myAnalysis):
        year = '16'
    elif('17' in myAnalysis):
        year = '17'
    elif('18' in myAnalysis):
        year = '18'

    if(year==''):
        print('You must specify a year in the first argument of makePileupHist')
        exit(0)
        
    certLumi = LumiList.LumiList(filename = certJSON[year])
    # certLumi = LumiList.LumiList(filename = certJSON[myAnalysis.split('_')[0].replace('UL20','')])
    print('creating PileupHistogram for '+myAnalysis)
    pileuplatest={
        '16':'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt',
        '18':'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PileUp/pileup_latest.txt',
        '17':'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PileUp/pileup_latest.txt',
    }

    # Runs={
    #     # 'F':[278509, 278770]#preVFP
    #     'F':[278801, 278802,278803, 278804, 278805, 278808],#postVFP
    #     'H':[283946,283934,283885]
    #     # #2017 1/fb dataset
    #     # 'C':[299481,299480,299479,299478,299477,299593,299594,299595,299597],
    #     # 'F': [306459,306456,305064,306125],
    #     # #2018 1/fb dataset
    #     # # 'B':[317626,317640,317641],
    #     # # 'D':[324021,324022,324077,325101],
    #     # 'A': [315420],
    #     # 'B': [317626, 317640, 317641, 317182],
    #     # 'C': [320065],
    #     # 'D': [324021, 324022, 324077, 325101],
    #     }

    # usedRuns=[]
    # for Run_s in myAnalysis.split('_')[1].replace('Run',''):
    #     usedRuns+=Runs[Run_s]

    (certLumi&LumiList.LumiList(runs=usedRuns)).writeJSON(fileName=myAnalysis+'.json')

    # pileuplatestLList=LumiList.LumiList(pileuplatest[myAnalysis.split('_')[0].replace('UL20','')])
    pileuplatestLList=LumiList.LumiList(pileuplatest[year])

    #pileupCalc.py:253 has a bug/typo, which already has been fixed for 102x but hasnt been rolled out apparently
    command="./mypileupCalc.py -i %s --inputLumiJSON %s --calcMode true --minBiasXsec 69200 --maxPileupBin 100 --numPileupBins 100 %s.root --verbose"%(myAnalysis+'.json',pileuplatest[year],myAnalysis)
    print(command)
    os.system(command)


if(__name__=='__main__'):
    analyses = []

    # analyses.append(('UL2018ABCD',[
    #     315420,                 # RunA
    #     317626, 317640, 317641, 317182, # RunB
    #     320065,                         # RunC
    #     324021, 324022, 324077, 325101  # RunD    
    # ]))

    
    # analyses.append(('UL2016_RunFH_postVFP',[
    #     278801, 278802,278803, 278804, 278805, 278808, #RunF
    #     283946,283934,283885 #RunH
    # ]))
    # analyses.append(('UL2016_RunF_preVFP',[
    #     278509, 278770
    # ]))

    analyses.append(('UL16_RunF_preVFP',[278509,278770]))
    analyses.append(('UL16_RunF_postVFP',[278801,278802,278803,278804,278805,278808]))
    
    # analyses.append(('UL16_RunAtoF',
    #                 range(271036,271658+1)+    # Run2016A
    #                 range(272007,275376+1)+    # Run2016B
    #                 range(275657,276283+1)+    # Run2016C
    #                 range(276315,276811+1)+    # Run2016D
    #                 range(276831,277420+1)+    # Run2016E
    #                 range(277772,278808+1)    # Run2016F
    # ))
    # analyses.append(('UL16_RunGtoH',
    #                 range(278820,280385+1)+    # Run2016G
    #                 range(280919,284044+1)    # Run2016H
    # ))

    # Run2016A	271036	271658
    # Run2016B	272007	275376
    # Run2016C	275657	276283
    # Run2016D	276315	276811
    # Run2016E	276831	277420
    # Run2016F	277772	278808
    # Run2016G	278820	280385
    # Run2016H	280919	284044
    for args in analyses:
        makePileupHist(*args)

    # for analysis in ['UL2017_RunC','UL2017_RunCF','UL2017_RunBD']:
    # for analysis in ['UL2018_RunB','UL2018_RunD','UL2018_RunBD']:
    # for analysis in ['UL2016_RunFH']:
    #     makePileupHist(analysis)
