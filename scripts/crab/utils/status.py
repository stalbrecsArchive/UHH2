import os,sys,glob

total,finished = 0,0
command='python /nfs/dust/cms/user/albrechs/UHH2/10_2/CMSSW_10_2_10/src/UHH2/scripts/crab/mcrab.py'
print command
with open('crab_status.log','r') as file:
    for line in file:
        if 'finished' in line:
            total+=int(line.split('/')[1].split(')')[0].strip())
            finished+=int(line.split('/')[0].split('(')[1].strip())
    with open('/afs/desy.de/user/a/albrechs/crab_monitor.log~','w') as output:
        # output.write('total: %i | finished: %i (%.2f%%)'%(total,finished,float(finished)/float(total)))
        output.write('%i %i %.2f'%(total,finished,100*float(finished)/float(total)))
        output.close()
    file.close()
