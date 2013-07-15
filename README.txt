Rohan Agrawal, UNI: ra2616
Digvijay Singh, UNI: ds3161

List of Files:-----------------------------------------------------------------------

run.sh                  :       Run file for rule mining
ra2616HW3.py            :       Association rule mining python file
ra2616-HW3CleanData.py  :       Cleans the data (from file WebExtract.csv into test.csv)
example-run.txt         :       Output of an interesting run
Dataset.csv             :       Integrated Data set file
Cuisine.txt             :       File containing Cuisine code and associated cuisine name

How to Run:--------------------------------------------------------------------------

1.Go to the directory ra2616-proj3 and type: 

python ra2616HW3.py Dataset.csv <support> <confidence>

2.Alternatively,you can run the program through our makefile 'run.sh' in the following way:

chmod +x run.sh
./run.sh Dataset.csv <support %> <confidence %>

For e.g if you want support of 50% and confidence of 50% you would run
./run.sh Datatest.csv 0.5 0.5

Dataset chosen:-----------------------------------------------------------------------

We have chosen the new york city restaurant insepction dataset.
Link for the dataset is http://www.nyc.gov/html/doh/downloads/zip/bigapps/dohmh_restaurant-inspections_002.zip , it contains data listing the restaurants in new york city, their cuisine, the borough in which they are in, and thier sanitary grade.

Data Cleaning:-----------------------------------------------------------------------

1. In the above zip file, the data is contained in WebExtract.txt. We have converted the file into an csv file.
2. The data set contained the following columns: CAMIS, DBA, BORO, BUILDING, STREET, ZIPCODE, PHONE, CUISINECODE, INSPDATE, ACTION, VIOLCODE, SCORE, CURRENTGRADE, GRADEDATE, RECORDDATE
3. We have retained only the columns BORO, CUISINECODE and CURRENTGRADE as we wanted to find interesting relations between these 3 fields.
4. We have removed the records which are empty for any of the 3 fields.
5. The column BORO contains borough code, which is decoded in the file RI_Webextract_BigApps_Latest.xls. We have replaced the borough code by the name of the associated borough. 
6. The colome CUISINECODE contains cuisine code which is decoded in Cuisine.txt. We have replaced the cuisine code by the name of the corresponding cuisin. Both tasks in (6) and (7) are done through the file ra2616-HW3CleanData.py. The file uses Cuisine.txt to read the cuisine code 

Internal design of the project:-----------------------------------------------------------------------

1. We implemented Apriori algorithm exactly as given in the paper "Fast algorithms for Mining Association Rules" sections 2.1 and 2.1.1.
2. First we calculated candidate itemsets of size 1 and then depending upon if they satisified minimum support criteria, we added them in the set of large itemsets (of size 1).
3. The functions getSupport() and getConfidence() calculate the Support and Confidence of itemsets/rules respectively according to the standard formulae. Support of an itemset is the fraction of times it appears in the dataset. Confidence of an association rule LHS=>RHS is equal to Support(LHS union RHS)/Support(LHS).
4. Large itemsets (L[k]) is calculated from smaller itemsets L[k-1] as given in Section 2.1.1 of the Research Paper. A join operation is done , where L[k-1] is joined with itself such that in the resulting L[k],k-2 elements should be common from the two L[k-1] itemsets.
5. Once this is done, pruning is the next important step where we remove all those large itemsets (in L[k])newly formed, whose any subset is not present in L[k-1]. This removes noise.
6. Now we have our large itemset. To form the association rules from the large itemset, we take all these sets and generate permutations from them (such that atleast one item is present in the RHS of any rule). We keep only those permutations in the rules whose confidence exceeds the given threshold value.
7. Thus we have our association rules which we output to output.txt

Why our dataset is interesting:-----------------------------------------------------------------------

We had an intuition that certain types of restaurants are concentrated in certain boroughs in new york city. Also we wanted to see if connections existed between certain types of cuisines and sanitary grades. We also wanted to see the borough with maximum number of A grade restaurants.

Interesting Run:-----------------------------------------------------------------------

/run.sh Dataset.csv 0.005 0.55
Support: 0.5%
Confidence: 55%

Interesting Rules:-----------------------------------------------------------------------

[Ice Cream Gelato Yogurt Ices] => [A] (Conf: 80.5%, Supp: 0.6%)
"Ice Cream Gelato Yogurt Ices" as a cuisine type has the highest percentage of A grade restaurants.

[French] => [MANHATTAN] (Conf: 79.8%, Supp: 0.9%)
Most french restaurants in New York City are in Manhattan.

[American,STATENISLAND] => [A] (Conf: 67.4%, Supp: 0.5%)
Most American restaurants in Staten Island have the sanitary grade of A

[Korean] => [QUEENS] (Conf: 62.7%, Supp: 0.7%)
Most Korean restaurants in New York City are in Queens. The high confidence of this rule is quite surprising.

[Japanese] => [MANHATTAN] (Conf: 60.3%, Supp: 1.9%)
Most Japanese restaurants in New York City are in Manhattan.

[B,Japanese] => [MANHATTAN] (Conf: 58.4%, Supp: 0.6%)
The most B Sanitary Grade Japanese Restaurants are in Manhattan.

[STATENISLAND] => [A] (Conf: 62.5%, Supp: 2.2%)
We though Manhattan would have highest percentage of A grade restaurants, but it turned out to be Staten Island.

[Jewish/Kosher] => [BROOKLYN] (Conf: 55.1%, Supp: 0.7%)
Most Jewish restaurants in New York City are in Brooklyn. This was definitely something new learnt!

References:--------------------------------------------------------------------------

1. Agrawal, R., & Srikant, R. (1994, September). Fast algorithms for mining association rules. In Proc. 20th Int. Conf. Very Large Data Bases, VLDB (Vol. 1215, pp. 487-499).
