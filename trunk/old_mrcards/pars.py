from pickle import load, dump

#dump(pars, open('/tmp/mrcards.dump', 'w'))
pars = {'theme':'default','rules':'culo','players':'player 1,player 2,player 3,player 4'}
try:
    pars2 = load(open('/tmp/mrcards.dump', 'rb'))
    for key,value in pars2.items():
        pars[key]=value
except:pass

print "\n\n\ncargado pars:",pars

#os.environ['HOME']
