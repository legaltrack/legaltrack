# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:50:55 2020

@author: Ghulam Mursaleen
"""

import pandas as pd
from fuzzywuzzy import process,fuzz

Filename="./contractCollection.csv"
df = pd.read_csv(Filename)

result=[]
####################input parameters##################
#cont_type="Catering Services ";
clause_category="Intro Text";
tag="Neutral";
cont_type="";
#clause_category="";
#tag="";
#text="whose principal place of residence is at / a [CORPORATE JURISDICTION] corporation with its principal place of business at] [PARTY B ADDRESS] (the ""[PARTY B ABBREVIATION]"").(The capitalized terms used in this agreement, in addition to those above";
text=""
no_of_records=1
"""
pd.read_csv('file_name.csv', usecols= ['column_name1','column_name2'])"""
if cont_type!="" and clause_category!="":
    contain_values = df[df['name'].str.contains(cont_type)   ]
    result=contain_values[df['ClausesCategories'].str.contains(clause_category)]
    if (len(result))==0:
            result=[1,2]
elif cont_type!="":
        result = df[df['name'].str.contains(cont_type)   ]
        if (len(result))==0:
            result=[1,2]
elif clause_category!="":
        result=df[df['ClausesCategories'].str.contains(clause_category)]
        if (len(result))==0:
            result=[1,2]
else:
    result=[1,2]
print ("result",len(result))

if len(result)>0:
    Filename="./ClausesCategoriesCollection.csv"
    df2 = pd.read_csv(Filename)
    if clause_category!="":#########if category is empty
        contain_values = df2[df2['name'].str.contains(clause_category)   ] ##if caluse category exist
        if len(contain_values)>0:
             ids=int(contain_values["_id"])
             Filename="./ClauseCollection.csv"
             df3 = pd.read_csv(Filename)
             #df3['clauseID']=pd.to_numeric(df3['clauseID'])
             rows=df3.loc[(df3['tags'] == tag) &(df3['clauseID'] == ids)]
             data=[]
             for index, row in rows.iterrows():
                 if (len(data)<no_of_records*10):
                     print("row",row["_id"])
                     data.append({"name":row["name"],"description":row["description"]})
             print("data",data)
             ####return data
             #print("rows",rows,df3.dtypes)
        elif tag!="":  ####################if category does not exist in records but tag exist 
             #ids=int(contain_values["_id"])
             Filename="./ClauseCollection.csv"
             df3 = pd.read_csv(Filename)
             #df3['clauseID']=pd.to_numeric(df3['clauseID'])
             rows=df3.loc[(df3['tags'] == tag)]
             data=[]
             for index, row in rows.iterrows():
                 if (len(data)<no_of_records*10):
                     print("row",row["_id"])
                     data.append({"name":row["name"],"description":row["description"]})
                 else:
                     break
             print("data tag exist",data)
             ####return data
        elif text!="":#########tag does not exist but text exist
             Filename="./ClauseCollection.csv"
             df3 = pd.read_csv(Filename)
             entities=df3['name'].tolist()
             descriptions=df3['description'].tolist()
             results=process.extract(text, descriptions, scorer=fuzz.token_sort_ratio)
             #print(results)
             data=[]
             print(results[0][0],results[0][1])
             for x in results:
                 if (len(data)<no_of_records*10):
                     data.append({"name":entities[descriptions.index(x[0])],"description":x[0]})
                     
                 else:
                     break
             print("data",data)
        else: ############if text not exist
            print("g aya no")
            
    elif tag!="": ############if clause category does not exist but tag exist
             Filename="./ClauseCollection.csv"
             df3 = pd.read_csv(Filename)
             #df3['clauseID']=pd.to_numeric(df3['clauseID'])
             rows=df3.loc[(df3['tags'] == tag)]
             data=[]
             for index, row in rows.iterrows():
                 if (len(data)<no_of_records*10):
                     print("row",row["_id"])
                     data.append({"name":row["name"],"description":row["description"]})
             print("data if tag exist only",len(data))
    elif text!="":#########tag does not exist but text exist
             Filename="./ClauseCollection.csv"
             df3 = pd.read_csv(Filename)
             entities=df3['name'].tolist()
             descriptions=df3['description'].tolist()
             results=process.extract(text, descriptions, scorer=fuzz.token_sort_ratio)
             #print(results)
             data=[]
             print(results[0][0],results[0][1])
             for x in results:
                 if (len(data)<no_of_records*10):
                     data.append({"name":entities[descriptions.index(x[0])],"description":x[0]})
                     
                 else:
                     break
             print("data",data)
    else: ############if text not exist
        print("g aya no")
        
        