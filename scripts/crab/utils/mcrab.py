#!/usr/bin/env python
##
##This Script will not work for the same tasks as multicrab.py
##It was written as a workaround for tasks with datetime in requestname
##
##  !!!!!Only use options like xml for tasks with datetime in requestname!!!!!
##
## Use multicrab.py for new tasks and the rest.
## 
import os,sys,glob
from create_dataset_xmlfile import create_dataset_xml
from readaMCatNloEntries import readEntries

data=True
command='status'
argv=sys.argv
print argv
if len(argv)<2:
    crabTasks=glob.glob('crab_Test/*')
elif '/' not in argv[1]:
    crabTasks=argv[2:]
    command = argv[1]
elif '/' not in argv[-1]:
    crabTasks=argv[1:-1]
    command=argv[-1]
else:
    crabTasks=argv[1:]
crabTasks.sort()
print '\n'
print 'tasks:',crabTasks
if len(crabTasks)<2 and not os.path.exists(crabTasks[0]):
    crabTasks=glob.glob(crabTasks[0]+'*')
    crabTasks.sort()
    print 'autocompleting ->',crabTasks
print 'command:',command
for task in crabTasks:
    taskname=task.split('/')[1]
    print (len(taskname)+120)*'-'
    print 60*'-'+taskname+60*'-'
    print (len(taskname)+120)*'-'
    # if('xml' in command):
    #     print 'creating xml-file...'
    #     dirname = '/pnfs/desy.de/cms/tier2/store/user/salbrech/RunII_102X_v1/'+('2016v3'if '2016' in taskname else '2017v2')+'/'+taskname.split('_')[1]+'/'+taskname+'/**/**/*.root'
    #     xmlname=('DATA_' if data else 'MC_')
    #     xmlname+=taskname.split('_')[1]+'_'
    #     xmlname+=taskname.split('_')[2]+'_'
    #     xmlname+=taskname.split('_')[3]
    #     xmlname+=('_'+taskname.split('_')[4] if ('v' in taskname.split('_')[4]) else '')
    #     xmlname+=('_17Jul2018' if '2016'in taskname else '_31Mar2018')
    #     xmlname+='.xml'
    #     print 'For',xmlname 
    #     print 'getting number of Entries from all Files in XML:'
    #     print 'in',dirname
    #     create_dataset_xml(dirname,xmlname)
    #     result_list = readEntries(4,[xmlname],True)
    # else:
    print 'crab '+command+' -d '+task
    os.system('crab '+command+' -d '+task)
    print '\n'
