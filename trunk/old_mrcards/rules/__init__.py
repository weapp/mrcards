import glob, os


path=__path__[0]+os.sep
for infile in glob.glob(path+"*.py"):
    filename, ext = os.path.splitext(infile)
    filename=filename[len(path):]
    if filename!='__init__':
        __builtins__['vars']()[filename]=os.path.splitext(infile)[0]
del path,ext,filename,glob,os,infile


def get_module(name):
    i=__import__('rules.'+name)
    return getattr(i,name) #on windows
    return __import__('rules'+os.sep+name) #on linux
