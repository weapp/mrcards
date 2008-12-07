import glob, os

def get_module(name):
    return __import__('rules'+os.sep+name)

"""
path=__path__[0]+os.sep
for infile in glob.glob(path+"*.py"):
    filename, ext = os.path.splitext(infile)
    filename=filename[len(path):]
    if filename!='__init__':
        __builtins__['vars']()[filename]=os.path.splitext(infile)[0]
del path,ext,filename,glob,os,infile

"""
