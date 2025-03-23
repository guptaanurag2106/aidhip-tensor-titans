from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

#Sends Customer Profile Info
@app.route('/cust_profile', methods=['GET'])
def cust_prof():
    cust_id = request.values.get('cust_id') # check naming
    
    cust_prof_dict = {}
    cust_prof_df = pd.read_csv('../data/customer_profile.csv')
    # print(cust_prof_df)
    for index, row in cust_prof_df.iterrows():
        if row[0] == cust_id:
            for cols in cust_prof_df.columns:
                cust_prof_dict[cols] = row[cols]
            return jsonify(cust_prof_dict)
    return "Customer not found"

#Sends Customer Purchase History
@app.route('/cust_purch_hist', methods=['GET'])
def cust_purch_hist():
    cust_id = request.values.get('cust_id')

    cust_purch_hist_list = []
    cust_purch_hist_df = pd.read_csv('../data/customer_purchase.csv')
    # print(cust_purch_hist_df)
    for index, row in cust_purch_hist_df.iterrows():
        if row[1] == cust_id:
            cust_purch_hist_dict = {}
            for cols in cust_purch_hist_df.columns:
                cust_purch_hist_dict[cols] = row[cols]
            cust_purch_hist_list.append(cust_purch_hist_dict)
    if len(cust_purch_hist_list) > 0:      
        return jsonify(cust_purch_hist_list)
    return "No records found"

#Sends Customer Socal Media Info
@app.route('/soc_med', methods=['GET'])
def soc_med():
    cust_id = request.values.get('cust_id')

    soc_med_list = []
    soc_med_df = pd.read_csv('../data/social_media_record.csv')
    # print(soc_med_df)
    for index, row in soc_med_df.iterrows():
        if row[1] == cust_id:
            soc_med_dict = {}
            for cols in soc_med_df.columns:
                soc_med_dict[cols] = row[cols]
            soc_med_list.append(soc_med_dict)
    if len(soc_med_list) > 0:      
        return jsonify(soc_med_list)
    return "No records found"

#Sends/Receives Customer Support History
@app.route('/cust_sup_hist', methods=['GET', 'POST'])
def cust_sup_hist():
    
    #Send
    if request.method == 'GET':
        cust_id = request.values.get('cust_id') # check naming
        print('cust id: ', cust_id)
        cust_sup_hist_list = []
        cust_sup_hist_df = pd.read_csv('../data/customer_support_record.csv')
        # print(cust_sup_hist_df)
        for index, row in cust_sup_hist_df.iterrows():
            if row[1] == cust_id:
                cust_sup_hist_dict = {}
                for cols in cust_sup_hist_df.columns:
                    cust_sup_hist_dict[cols] = row[cols]
                cust_sup_hist_list.append(cust_sup_hist_dict)
        if len(cust_sup_hist_list) > 0:      
            return jsonify(cust_sup_hist_list)
        return "No records found"
    
    #Receive
    elif request.method == 'POST':
        cust_sup_hist_record = request.get_json()
        cust_sup_hist_df = pd.DataFrame(columns=['complaint_id','customer_id','date','transcript','main_concerns','is_repeating_issue','was_issue_resolved', 'sentiment'])
        for col in cust_sup_hist_record:
            cust_sup_hist_df[col] = [cust_sup_hist_record[col]]
        cust_sup_hist_df.to_csv('../data/customer_support_record.csv', mode='a', header=False, index=False)
        return "Record added"

if __name__ == '__main__':
    app.run(debug=True)