import os,sys,glob

idun,failed,total,finished,running = 0,0,0,0,0
command='python /nfs/dust/cms/user/albrechs/UHH2/10_2/CMSSW_10_2_10/src/UHH2/scripts/crab/mcrab.py'
print command
tasks=0
with open('crab_status.log','r') as file:
    for line in file:
        if 'task name' in line.lower():
            tasks+=1            
        if 'finished' in line:
            total+=int(line.split('/')[1].split(')')[0].strip())
            finished+=int(line.split('/')[0].split('(')[1].strip())
        if 'running' in line:
            running+=int(line.split('/')[0].split('(')[1].strip())
        if 'failed' in line and '%' in line and 'please' not in line:
            failed+=int(line.split('/')[0].split('(')[1].strip())
        if 'idle' in line or 'unsubmitted' in line:
            idun+=int(line.split('/')[0].split('(')[1].strip())
    print "(%i/%i) running and (%i/%i) finished and (%i/%i) failed (%.2f %%) in %i tasks"%(running,total,finished,total,failed,total,float(failed)/float(total)*100,tasks)
    print idun, "jobs are unsubmitted or idle"
    file.close()
