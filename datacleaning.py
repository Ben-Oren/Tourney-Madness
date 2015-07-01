import pandas as pd
import numpy as np
from scipy.stats import ttest_rel

import string
import re
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path1 = "bball/confdata.txt"
abs_file_path1 = os.path.join(script_dir, rel_path1)
rel_path2 = "bball/dancedata.txt"
abs_file_path2 = os.path.join(script_dir, rel_path2)
rel_path3 = "bball/descreptest.txt"
abs_file_path3 = os.path.join(script_dir, rel_path3)
rel_path4 = "bball/alldancedata.txt"
abs_file_path4 = os.path.join(script_dir, rel_path4)


#open file as text, stick each line into a list
#create list "test" to test with
conftxt = open(abs_file_path1, "r")
conflines = conftxt.readlines()
dancetxt = open(abs_file_path2, "r")
dancelines = dancetxt.readlines()
allconftxt = open(abs_file_path3, "r")
allconflines = allconftxt.readlines()
alldancetxt = open(abs_file_path4, "r")
alldancelines = alldancetxt.readlines()
#data = pd.DataFrame(lines)
#test = data.ix[0:13,:]
#print test

#split lines into individual data units: team, conf, year, result; turn string numbers into digits

def units(lines):
    nums = {}
    for x in range(0,17):
        nums[str(x)] = str(x)
    for line in lines:
        index = lines.index(line)
        #for key in nums.keys():
        #    line = re.sub(r'\b%s\b'%(key), '"%s"'%(nums[key]), line)
        line = line.split(r'"')
        lines[index] = line
    return lines
    
conflines = units(conflines)
dancelines = units(dancelines)
allconflines = units(allconflines)
alldancelines = units(alldancelines)

#remove data units that aren't data (ie, the punctuation units)
def rem_punct(line):
    for word in line:
        if re.search(r'\w', word) == None:
            index = line.index(word)
            del line[index]
        word = re.sub(r'\b,\b', '', word)
        word = re.sub(r'^:\b', '', word)
    return line
    
conflines = map(lambda x: rem_punct(x), conflines)
dancelines = map(lambda x: rem_punct(x), dancelines)
allconflines = map(lambda x: rem_punct(x), allconflines)
alldancelines = map(lambda x: rem_punct(x), alldancelines)

conflines = map(lambda x: rem_punct(x), conflines)
dancelines = map(lambda x: rem_punct(x), dancelines)
allconflines = map(lambda x: rem_punct(x), allconflines)
alldancelines = map(lambda x: rem_punct(x), alldancelines)

#print allconflines[0:6]
test = alldancelines[0:6]

#turn the string(which looks liks "item: value, item: value") into a dictionary
def str2dict(collection):
    dictlist = []
    for line in collection:
        if len(line)>3:
            dictionary = {}
            dictionary[line.pop(0)] = line.pop(1)
            dictionary[line.pop(0)] = line.pop(1)
            dictionary[line.pop(0)] = line.pop(1)
            dictionary[line.pop(0)] = line.pop(1)
            dictlist.append(dictionary)
    return dictlist
    
def str2dict2(collection):
    dictlist = []
    for line in collection:
        if len(line)>5:
            dictionary = {}
            for x in range(0, len(line)-1, 2):
                dictionary[line[x]] = line[x+1]
            dictlist.append(dictionary)
        return dictlist
        
def dancelines2dict(collection):
    dictlist = []
    for line in collection:
        if len(line)>5:
            dictionary = {}
            for x in range(0, len(line)-1, 2):
                dictionary[line[x]] = line[x+1]
            dictlist.append(dictionary)
    return dictlist
        
conflines = str2dict(conflines)
dancelines = str2dict(dancelines)
allconflines = dancelines2dict(allconflines)
alldancelines = dancelines2dict(alldancelines)




#dataframe that shit
confdata = pd.DataFrame(conflines)
dancedata = pd.DataFrame(dancelines)
allconfdata = pd.DataFrame(allconflines)
alldancedata = pd.DataFrame(alldancelines)

#print confdata.info()
#print dancedata.info()
#print allconfdata.info()
#print alldancedata.head()

#print allconfdata.head()

#fixing the results column in conf and dance frames (currently ": 'data', ")
numresult = confdata.iloc[:, 1]
confdata.iloc[:, 1] = [x[2] for x in numresult]
numresult = dancedata.iloc[:, 1]
dancedata.iloc[:, 1] = [x[2] for x in numresult]
numresult = allconfdata.iloc[:, 2]
allconfdata.iloc[:, 2] = [x[2] for x in numresult]
numresult = alldancedata.iloc[:, 1]
alldancedata.iloc[:, 1] = [x[2] for x in numresult]

#sorting by conference, team, year
confdata = confdata.sort(["conf", "year", "team"])
dancedata = dancedata.sort(["myear", "mteam"])
allconfdata = allconfdata.sort(["conf", "year", "team"])
alldancedata = alldancedata.sort(["myear", "mteam"])




#print confdata.head(20)
#print confdata.tail(20)
#print dancedata.head(20)
#print dancedata.tail(20)
#print confdata.info
#print dancedata.info


#print conftdata.info()
#print conftdata.iloc[13:30, :]
#print dancetdata.info()
#print dancetdata.iloc[114:116, :]


#merging the conference and march madness data; outer join keeps rows in one dataframe that don't have values in the other
testdata = pd.merge(confdata, dancedata, how = "outer", on = None, left_on = ("year", "team"), right_on = ("myear", "mteam"), left_index = False, right_index = False)

alltestdata = pd.merge(allconfdata, alldancedata, how = "outer", on = None, left_on = ("year", "team"), right_on = ("myear", "mteam"), left_index = False, right_index = False)

#print alltestdata.head()
#print testdata.head()
#print alltestdata.info()


#reordering columns so that the two team and year columns are by each other
testdata = testdata[["conf", "result", "team", "mteam", "year", "myear", "mrank", "mresult"]]

alltestdata = alltestdata[["conf", "regchamp", "tournchamp", "result", "mrank", "mresult", "team", "year", "mteam", "myear"]]

#alltestdata.loc[:, "mresult"] = map(lambda x: int(x), alltestdata.loc[:, "mresult"])

#sorting by regchamps / nonreg champs

alltestdata = alltestdata.sort(["regchamp", "tournchamp"])

#print alltestdata.describe()

test = alltestdata

#test.index = range(0, len(test))

#print test.tail()

#print alltestdata.head()
#print test.describe()

#print test.unique

#test.ix[:, "mresult"] = test.ix[:, "mresult"].dropna()

#print test.describe()

#print test.describe()

#print test.ix[49,:]

change = ["result", "mrank", "mresult"]

for x in change:
    test.ix[:, x] = test.ix[:, x].astype(float)


#print test.ix[:, "result"].mean()
#print test.ix[:, "mrank"].mean()
#print test.ix[:, "mresult"].mean()

#print test.ix[:, "mresult"].mean()


#testtournrank = test["mrank"].groupby(test["tournchamp"])

#print testtourn.mean()

#testtournresult = test["result"].groupby(test["regchamp"])

#print testtournresult.mean()

testtournmresult = test["mresult"].groupby([test["tournchamp"], test["regchamp"]])

#print testtournmresult.describe() 

#print testtournmresult.groups.keys()

print testtournmresult.groups[("N", "N")]




#f = lambda x: int(x)

#tourngroup_dance = tourngroup["mresult"].apply(f)

#print tourngroup

#print tourngroup.agg([np.mean, np.std])
#print tourngroup_dance.agg([np.mean, np.std])

#print tourngroup["mresult"].agg([np.mean])

#print tourngroup.aggregate(np.mean)

#print testdata.ix[160:, 2:6]

#print [testdata.ix[x, "myear"] != testdata.ix[x, "year"] for x in range(0,171)] 














#KEEEP THISSSSSS!!!!!!!!!creating list for big dance url scraping
def teamyearurl(teamlist, yearlist):
    list = []
    #creating list; appending "19" or "20" to last two digits of year
    for num in range(len(teamlist)):
        list.append([teamlist[num], yearlist[num][5:7]])
        if list[num][1] == "98" or list[num][1] == "99":
            list[num][1] = re.sub(list[num][1], "19"+list[num][1], list[num][1])
        else:
            list[num][1] = re.sub(list[num][1], "20"+list[num][1], list[num][1])
    return list
    
    
    
#NEED TO KEEP teamyear SO SPIDERS WILL WORK!!!!ONE!!!!1!!!!    
teamyear = teamyearurl(allconfdata.ix[:,"team"], allconfdata.ix[:, "year"])

#print confdata.head()

print 

#print dancedata.head()


















alldancetxt.close()
allconftxt.close()
conftxt.close()
dancetxt.close()