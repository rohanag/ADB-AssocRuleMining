from __future__ import division
import itertools  
import sys

#  Interesting run
# support = 0.005
# confidence = 0.50

#Taking arguments from command line with error checking
support = float(sys.argv[2])
confidence = float(sys.argv[3])
filename = sys.argv[1]
if support>1 or support<0:
    print "Please enter a support value between 0 and 1.Exiting......"
    exit()
if confidence>1 or confidence<0:
    print "Please enter a confidence value between 0 and 1.Exiting...."
    exit()

#Returns support of an itemset(containing one or more items)
def getSupport(item):
    count = 0
    for row in trans:
        flag = 0
        for i in item:
            if i not in row:
                flag = 1
                break
        if flag == 0:
            count += 1
    return count/len(trans)
    
#Returns the confidence of an association rule according to the below formula:
#Confidence of LHS=>RHS is equal to Support(LHS union RHS)/Support(LHS)
def getConfidence(rule):
    return getSupport(rule[1] + rule[0])/getSupport(rule[0])
    
#Returns the pruned itemset.This basically involves deleting an itemset from the set of large itemsets L[k] if any of the subsets of that itemset is absent in L[k-1].
def prune(item, l):
    for i in itertools.permutations(item,len(item)-1):
        #Checking presence of the subset in L[k-1]
        if set(list(i)) not in [set(x) for x in l]:
            return False
    return True

f = open(filename) #Opening the dataset file
trans = []
rules = [] #For storing the association rules
counter = 0
for i in f:
    trans.append([x.strip() for x in i.strip().split(',') if x])
    counter += 1

#Calculating candidate itemset of size 1 separately .
c1 = set() #Candidate item set of size 1
for i in trans:
    c1 = c1.union(set([x for x in i]))
c1 = list(c1)
c1 = [[x] for x in c1]

l1 = [] #Large itemset of size 1
#Candidate itemset enters the set of large itemsets only if it satisfies the threshold for minimum support
for c in c1:
    if getSupport(c) > support:
        l1.append(c)

#Calculating candidate and hence large itemsets starting from k=2
l = {}
c = {}
l[1] = l1
c[1] = c1
k = 2
while l[k-1]: 
    #Joining L[k-1] with L[k-1] to generate L[k],as told in the "join" step of Section 2.1.1 of the Research Paper 
    slicedl = [x[0:k-2] for x in l[k-1]]  #Extracting k-2 elements from L[k-1] for the where clause of the join statement
    l[k] = []
    c[k] = []
    for i in range(len(slicedl)):
        for j in range(i+1,len(slicedl)):
            if slicedl[i] == slicedl[j]:
                temp = set( l[k-1][i] + l[k-1][j] )
                if prune(list(temp),l[k-1]) == True:
                    c[k].append(list(temp))

    #Getting Large Itemsets from  Candidate itemsets based on minimum support threshold
    for i in c[k]:
        if getSupport(i) > support:
            l[k].append(i)

    k += 1

#Removing duplicate rules of the type: [A,B]=>[C] and [B,A]=>[C]
lastelements = []
for i in range(2,k):
    for j in l[i]:
        for k in itertools.permutations(j):
            if [k[-1],set(k)] in lastelements:
                continue
            lastelements.append([k[-1],set(k)])
            if getConfidence([list(k[:-1]),[k[-1]]]) > confidence:
                rules.append([list(k[:-1]),[k[-1]]])


#Printing to file
o = open("output.txt",'w')

#Sorting outputs of Large Itemsets according to specification given in question
sortedl = []
for i in l:
    for j in l[i]:
        sortedl.append((getSupport(j)*100,j))

sortedl.sort(reverse = True)
print >>o,'== Large itemsets (min_sup=%.1f%%)' % (support*100)
for s in sortedl:
    print>>o, "[%s], %.1f%%" % (",".join(s[1]),s[0])
    
#Sorting outputs of Association Rules according to specification given in question
sortedrules = []
for r in rules:
    sortedrules.append((getConfidence(r)*100, getSupport(r[0]+r[1])*100,r ))
print >>o
print >>o
print >>o,'==High-confidence association rules (min_conf=%.1f%%)' % (confidence*100)
sortedrules.sort(reverse = True)
for s in sortedrules:
    print >>o,"[%s] => [%s] (Conf: %.1f%%, Supp: %.1f%%)" % (",".join(s[2][0]),s[2][1][0],s[0],s[1])
    
f.close()

