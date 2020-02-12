import os,sys,json
import subprocess

def checkDataset(dataset):
    # das_query='file dataset=%s'%dataset
    print '|'+dataset
    das_query=dataset
    dasgoclient_template='dasgoclient -query "%s" -json'
    p=subprocess.Popen([dasgoclient_template%das_query],shell=True,stdout=subprocess.PIPE)
    out=p.communicate()[0]
    out_json=json.loads(out)

    TotalSize=0
    NEvents=[]
    datasets=set()
    for dataset in out_json:
        datasets.add(dataset['dataset'][0]['name'])

    for dataset in datasets:
        print '|_'+dataset
        das_query='file dataset=%s'%dataset
        process=subprocess.Popen([dasgoclient_template%das_query],shell=True,stdout=subprocess.PIPE)
        outputS=process.communicate()[0]
        output=json.loads(outputS)
        for f in output:
            N=f['file'][0]['nevents']
            TotalSize+=float(f['file'][0]['size'])
            NEvents.append(N)
            NEvents.sort()
        print TotalSize
    print 'N Files:',len(NEvents)
    print 'Total Size %.2f TB'%(TotalSize/1024./1024./1024./1024.)
    print 'smallest File:',NEvents[0],'Events  |  largest File:',NEvents[-1],"Events"
    print 'You should ask for at least %0.f minutes.'%(60.*float(NEvents[-1])/4000.)



datasets=['/JetHT/Run2016*-17Jul2018*/MINIAOD','/JetHT/Run2017*-31Mar2018*/MINIAOD']#,'/SingleMuon/Run2017D-MuTau-PromptReco-v1/RAW-RECO']
for dataset in datasets:
    checkDataset(dataset)


print '("..CRAB can only guarantee a maximum of 2750 minutes (~46 hours) so if it\'s larger than this, expect some job failures.")'
