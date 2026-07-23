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
os.chdir(r'C:\スリ\Python Programs')
# print(os.system("dir"))
# print(os.getcwd())
# os.makedirs(name='Sample',exist_ok=True)
# os.rename('Sample','sample')
# os.removedirs('sample')
# os.startfile(samplePath)
# os.startfile('https://github.com/srirengasarathy13')
# with open('file1.txt','w') as f1:f1.write('Hello, World!')
# os.link('file1.txt','file2.txt')
# with open('file1.txt','a') as f1:f1.write('\nI am working at Agnie Consulting.')
# with open('file1.txt','r') as f1:print(f1.read())
print(os.cpu_count())