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

    datasets=set()
    for dataset in out_json:
        datasets.add(dataset['dataset'][0]['name'])

    for dataset in datasets:
        print '|_'+dataset
        das_query='site dataset=%s'%dataset
        process=subprocess.Popen(['dasgoclient -query "%s"'%das_query],shell=True,stdout=subprocess.PIPE)
        outputS=process.communicate()[0]
        print outputS



datasets=['/JetHT/Run2016*-17Jul2018*/MINIAOD','/JetHT/Run2017*-31Mar2018*/MINIAOD']#,'/SingleMuon/Run2017D-MuTau-PromptReco-v1/RAW-RECO']
for dataset in datasets:
    checkDataset(dataset)
