import os
from os import path
os.makedirs(name='CreatedByOs',exist_ok=True) #Create Directory
samplePath = r'C:\スリ\Python Programs\CreatedByOs'
print(path.exists(samplePath))
print(path.basename(samplePath))
print(path.expanduser('~/CreatedByPythonOS'))
print(path.dirname(samplePath))
print(os.getcwd())
print(os.getlogin())
