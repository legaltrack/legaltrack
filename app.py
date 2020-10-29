import flask
import csv

import pandas as pd
from fuzzywuzzy import process,fuzz
from werkzeug.utils import secure_filename
from flask import  abort,request,send_file,jsonify, make_response
from Untitled import Model
model=Model()

from flask_cors import CORS, cross_origin
app = flask.Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "Api is working for Legal Contracts";
@app.route('/search', methods = ['GET', 'POST'])
def search():
    
   if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
   elif request.method == 'GET':
      
      content = request.get_json()
      print(content)
      Filename="./contractCollection.csv"
      df = pd.read_csv(Filename)
    
      result=[]
      clause_category=content["clause_category"]
      tag=content["tag"];
      cont_type=content["cont_type"];
      text=content["text"];
      no_of_records=content["records"];
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
      #print ("result",len(result))
    
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
                 #print("data",data)
                 if len(data)==0:
                      rows=df3.loc[(df3['clauseID'] == ids)]
                      data=[]
                      for index, row in rows.iterrows():
                         if (len(data)<no_of_records*10):
                             print("row",row["_id"])
                             data.append({"name":row["name"],"description":row["description"]})
                      return _corsify_actual_response(jsonify(data))
                 return _corsify_actual_response(jsonify(data))
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
                         #print("row",row["_id"])
                         data.append({"name":row["name"],"description":row["description"]})
                     else:
                         break
                 #print("data tag exist",data)
                 return _corsify_actual_response(jsonify(data))
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
                 #print("data",data)
                 return _corsify_actual_response(jsonify(data))
            else: ############if text not exist
                #print("g aya no")
                return _corsify_actual_response(jsonify({}))
                
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
                 #print("data if tag exist only",len(data))
                 return _corsify_actual_response(jsonify(data))
        elif text!="":#########tag does not exist but text exist
                 Filename="./ClauseCollection.csv"
                 df3 = pd.read_csv(Filename)
                 entities=df3['name'].tolist()
                 descriptions=df3['description'].tolist()
                 results=process.extract(text, descriptions, scorer=fuzz.token_sort_ratio)
                 #print(results)
                 data=[]
                 #print(results[0][0],results[0][1])
                 for x in results:
                     if (len(data)<no_of_records*10):
                         data.append({"name":entities[descriptions.index(x[0])],"description":x[0]})
                         
                     else:
                         break
                 #print("data",data)
                 return _corsify_actual_response(jsonify(data))
        else: ############if text not exist
            return _corsify_actual_response(jsonify({}))
      #print(clause_category)
      #data = request.values
      #print("coming",request.form["id"])
      
      
      #id=str(request.form["id"])
      #print(id,type(id))
      #response=model.recommendation(id)
      
      
   else:
      return "error"

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    #response.headers.add('Access-Control-Allow-Headers', "*")
    #response.headers.add('Access-Control-Allow-Methods', "*")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port = 3000, threaded=True,debug=True, use_reloader=True)