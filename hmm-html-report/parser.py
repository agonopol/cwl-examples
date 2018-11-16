#!/usr/bin/env python
# coding: utf-8

# # Import
# 

import re
import math
import time
import os
import sys, getopt
from subprocess import call
from collections import Counter
# from IPython.display import HTML


# # Useful functions

# ## File read tools
# 

# In[4]:


def readInFile(fileName):
    with open(fileName, 'r') as f:
        content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
    return [x.strip() for x in content] 

def is_float(input):
  try:
    num = float(input)
  except ValueError:
    return False
  return True


# ## Datastructures
# 

# In[5]:


class HmmResult(object):
    name = ""
    intervall = ()
    profile = ""
    profileid = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, name, intervall, profile, profileid):
        self.name = name
        self.intervall = intervall
        self.profile = profile
        self.profileid = profileid


# ## Helper methods

# In[17]:


def getPlatName(input):
    result =[]
    for i in range(len(input)):
        if(not is_float(input[-i-1])):
            result.append(input[-i-1])
        else:
            break
    result.append(input[0])
    result.reverse()
    return ' '.join(result)

def getDatabaseDictionary(file):
    d ={}
    dataBase = readInFile(file)
    for i in range(0,len(dataBase),2):
        name = re.sub(r"\s+", " ", dataBase[i])[1:]
        sequence = dataBase[i+1] 
        d[name] = sequence
    return d 

def createFileName(resultPath, dataBasePath):
    timeFormat= "%Y-%m-%d_%H:%M:%S"
    resultName = os.path.basename(resultPath)
    databaseName = os.path.basename(dataBasePath)
    return str(time.strftime(timeFormat)) +"_" +resultName +"_"+ databaseName


# ## Parse Results
# 

# In[24]:


def getListOfHmmResults(fileName):
    result = []
    content= readInFile(fileName)
    for i in range (3,len(content)):
        if content[i][0] == '#':
            break
        else:
            
            hmmResult =re.split(r'\s{1,}', content[i])
            name = getPlatName(hmmResult)
            try:
                intervall = (hmmResult[19],hmmResult[20])
            except IndexError:
                 intervall = (0,0)
            profile = hmmResult[3]
            profileid = hmmResult[4]
            hmmresult = HmmResult(name.rstrip(), intervall, profile, profileid)
            result+=[hmmresult]
            #print(hmmresult.name + " "+str(hmmresult.intervall[0])+':'+str(hmmresult.intervall[1])+' ' +hmmresult.profile+
            #     " "+hmmresult.profileid)
    return result


# ## HTML file writer

# ### HTML higlighther

# In[15]:


def highlightSequence(sequence, intervalTuple): 
    start = '<span class="base0B">'
    end = '</span>'
    result =sequence.replace(sequence[intervalTuple[0]:intervalTuple[1]] , start + sequence[intervalTuple[0]:intervalTuple[1]] + end )    

    return result 

def highlightSequence2(sequence, profileTuple,aRnhTuple): 
    start = '<span class="base0B">'
    startARnh = '<span class="base0A">'
    end = '</span>'

    result =sequence.replace(sequence[profileTuple[0]:profileTuple[1]] , start + sequence[profileTuple[0]:profileTuple[1]] + end )
    aRnh= sequence[aRnhTuple[0]:aRnhTuple[1]]
    
    result =result.replace(aRnh , startARnh + aRnh + end )
    return result


# ### Test Run

# In[9]:


# listOfResult= getListOfHmmResults('allRepbaseArnhParseAble.out')


# In[12]:


# database = getDatabaseDictionary('allRepbase.fasta.TranslatedProtein.fasta')


# In[25]:


database=''
hmmresult=''
ofile=''
 
###############################
# o == option
# a == argument passed to the o
###############################
# Cache an error with try..except 
# Note: options is the string of option letters that the script wants to recognize, with 
# options that require an argument followed by a colon (':') i.e. -i fileName
#
try:
    myopts, args = getopt.getopt(sys.argv[1:],"h:d:r:o:")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -d proteindatabase -r hmmresult -o output" % sys.argv[0])
    sys.exit(2)
 
for o, a in myopts:
    if o == '-d':
        database=a
    elif o == '-r':
        hmmresult=a
    elif o == '-o':
        ofile=a
 
# Display input and output file name passed as the args
print ("database : %s result: %s and  output file: %s" % (database,hmmresult,ofile) )

dataBasePath = database 
resultPath = hmmresult
fileName =createFileName(resultPath, dataBasePath)
print(fileName)
listOfResult= getListOfHmmResults(resultPath)
dataBaseDictionary =  getDatabaseDictionary(dataBasePath)
i=0
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "template", "preamble.tpl")) as f:
    lines = f.readlines()
    with open(ofile, "w") as f1:
        f1.writelines(lines)
        for result in listOfResult:
            if result.name in dataBaseDictionary:
                with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "template", "panel.tpl")) as f:
                    lines1 = f.readlines()
                    stripName= "".join(result.name.split()) 
                    i+=1
                    intervall = (int(result.intervall[0]),int(result.intervall[1]))
                    expandedSequence =highlightSequence (dataBaseDictionary[result.name],intervall) 
                    line = lines1[0] % ("panel"+str(i), result.name + " Profile: "+                                       '<span class="base0B">'+ result.profile+ '</span>',                                        "panel"+str(i) , expandedSequence)
                    f1.write(line)
        f1.write("</body> </html>   ")


