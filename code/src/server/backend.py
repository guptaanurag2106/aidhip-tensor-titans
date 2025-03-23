from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route("/customer_ids", methods=["GET"])
def customer_ids():
    # read from the csv and return them
    df = pd.read_csv("../data/customer_profile.csv")
    return jsonify(df["customer_id"].tolist())

#Sends Customer Profile Info
@app.route('/customer_profile', methods=['GET'])
def cust_prof():
    customer_id = request.args.get('customer_id')
    cust_prof_df = pd.read_csv('../data/customer_profile.csv')

    for index, row in cust_prof_df.iterrows():
        print("row is ", row['customer_id'])
        if row['customer_id'] == customer_id:
            return jsonify(row.to_dict())
    return {"error": "Customer not found"}

#Sends Customer Purchase History
@app.route('/cust_purch_hist', methods=['GET'])
def cust_purch_hist():
    customer_id = request.args.get('customer_id')

    cust_purch_hist_list = []
    cust_purch_hist_df = pd.read_csv('../data/customer_purchase.csv')
    # print(cust_purch_hist_df)
    for index, row in cust_purch_hist_df.iterrows():
        if row[1] == customer_id:
            cust_purch_hist_dict = {}
            for cols in cust_purch_hist_df.columns:
                cust_purch_hist_dict[cols] = row[cols]
            cust_purch_hist_list.append(cust_purch_hist_dict)
    if len(cust_purch_hist_list) > 0:      
        return jsonify(cust_purch_hist_list)
    return {"error": "No records found"}

#Sends Customer Socal Media Info
@app.route('/soc_med', methods=['GET'])
def soc_med():
    customer_id = request.args.get('customer_id')

    soc_med_list = []
    soc_med_df = pd.read_csv('../data/social_media_record.csv')
    # print(soc_med_df)
    for index, row in soc_med_df.iterrows():
        if row[1] == customer_id:
            soc_med_dict = {}
            for cols in soc_med_df.columns:
                soc_med_dict[cols] = row[cols]
            soc_med_list.append(soc_med_dict)
    if len(soc_med_list) > 0:      
        return jsonify(soc_med_list)
    return {"error": "No records found"}

#Sends/Receives Customer Support History
@app.route('/customer_support_history', methods=['GET', 'POST'])
def cust_sup_hist():
    
    #Send
    if request.method == 'GET':
        customer_id = request.args.get('customer_id') # check naming
        
        cust_sup_hist_list = []
        cust_sup_hist_df = pd.read_csv('../data/customer_support_record.csv')
        # print(cust_sup_hist_df)
        for index, row in cust_sup_hist_df.iterrows():
            if row[1] == customer_id:
                cust_sup_hist_dict = {}
                for cols in cust_sup_hist_df.columns:
                    cust_sup_hist_dict[cols] = row[cols]
                cust_sup_hist_list.append(cust_sup_hist_dict)
        if len(cust_sup_hist_list) > 0:      
            return jsonify(cust_sup_hist_list)
        return {"error": "No records found"}
    
    #Receive
    elif request.method == 'POST':
        cust_sup_hist_record = request.get_json()
        cust_sup_hist_df = pd.DataFrame(columns=['complaint_id','customer_id','date','transcript','main_concerns','is_repeating_issue','was_issue_resolved', 'sentiment'])
        for col in cust_sup_hist_record:
            cust_sup_hist_df[col] = [cust_sup_hist_record[col]]
        cust_sup_hist_df.to_csv('../data/customer_support_record.csv', mode='a', header=False, index=False)
        return {"customer_id": cust_sup_hist_record['customer_id']}

if __name__ == '__main__':
    app.run(debug=True, port=5003)