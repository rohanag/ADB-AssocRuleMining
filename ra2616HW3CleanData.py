from __future__ import division


fil = open('WebExtract.csv')
cui = open('Cuisine.txt')
new = open('test.csv','w')
cuisine = {}
for i in cui:
    a = i.strip().split(',')
    b = int(a[0])
    c = ''.join(a[1:])
    cuisine[b] = c
print cuisine

#Replacing Borough code with Borough name in the dataset
for i in fil:
    a,b,c,d,e,f,g = [x.strip() for x in i.strip().split(',') if x]
    b = int(b)
    if b == 1:
        b = 'MANHATTAN'
    elif b == 2:
        b = 'BRONX'
    elif b == 3:
        b = 'BROOKLYN'
    elif b == 4:
        b = 'QUEENS'
    elif b == 5:
        b = 'STATENISLAND'
    else:
        print 'asdasd',b
        continue
    #Replacing cuisine code with Cuisine name,picked up from Cuisine.txt
    if int(e) in cuisine:
        e = cuisine[int(e)]
    else:
        print 'asd',e
        continue
    print >> new,a,',',b,',',c,',',d,',',e,',',f,',',g
new.close()
