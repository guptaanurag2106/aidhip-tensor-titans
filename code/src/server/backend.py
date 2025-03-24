from flask import Flask, request, jsonify
import pandas as pd
import csv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

INVALID_SENTIMENT_SCORE = -100

@app.route("/customer_ids", methods=["GET"])
def customer_ids():
    df = pd.read_csv("../data/customer_profile.csv")
    return jsonify(df["customer_id"].tolist())


@app.route('/customer_profile', methods=['GET'])
def cust_prof():
    customer_id = request.args.get('customer_id')
    df = pd.read_csv('../data/customer_profile.csv')

    for _, row in df.iterrows():
        if row['customer_id'] == customer_id:
            return jsonify(row.to_dict())
    return {"error": "Customer not found"}


@app.route('/customer_purchase_history', methods=['GET'])
def get_customer_purchase_history():
    customer_id = request.args.get('customer_id')
    matching_rows = []
    
    with open('../data/customer_purchase.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get('customer_id') == customer_id:
                row['amt'] = float(row['amt'])
                matching_rows.append(row)
    
    return jsonify(matching_rows)


@app.route('/customer_purchase_history', methods=['POST'])
def add_customer_purchase_history():
    data = request.get_json()
    data['customer_id'] = request.args.get('customer_id')
    with open('../data/customer_purchase.csv', mode='a', newline='') as file:
        cols = ['transaction_id','customer_id','date','platform','payment_method','amt','location','item_category','item_sub_category','item_brand']
        writer = csv.DictWriter(file, fieldnames=cols)
        writer.writerow(data)
    return {"customer_id": data['customer_id']}



@app.route('/customer_social_media_history', methods=['GET'])
def get_customer_social_history():
    customer_id = request.args.get('customer_id')
    matching_rows = []
    
    with open('../data/social_media_record.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get('customer_id') == customer_id:
                row['influencers_followed'] = float(row['influencers_followed'])
                row['sentiment_score'] = float(row['sentiment_score'])
                row['engagement_level'] = float(row['engagement_level'])
                matching_rows.append(row)
    
    return jsonify(matching_rows)


@app.route('/customer_social_media_history', methods=['POST'])
def add_customer_social_history():
    data = request.get_json()
    data['customer_id'] = request.args.get('customer_id')
    data['sentiment_score'] = INVALID_SENTIMENT_SCORE
    data['engagement_level'] = INVALID_SENTIMENT_SCORE
    data['brands_liked'] = INVALID_SENTIMENT_SCORE
    with open('../data/social_media_record.csv', mode='a', newline='') as file:
        cols = ['post_id','customer_id','date','platform','image_url','text_content','influencers_followed','topics_of_interest','feedback_on_financial_products','sentiment_score','engagement_level','brands_liked']
        writer = csv.DictWriter(file, fieldnames=cols)
        writer.writerow(data)
    return {"customer_id": data['customer_id']}


@app.route('/customer_support_history', methods=['GET'])
def get_customer_support_history():
    customer_id = request.args.get('customer_id')
    matching_rows = []
    cust_sup_hist_df = pd.read_csv('../data/customer_support_record.csv')
    for index, row in cust_sup_hist_df.iterrows():
        if row[1] == customer_id:
            cust_sup_hist_dict = {}
            for cols in cust_sup_hist_df.columns:
                cust_sup_hist_dict[cols] = row[cols]
            matching_rows.append(cust_sup_hist_dict)
    return jsonify(matching_rows)


@app.route('/customer_support_history', methods=['POST'])
def add_customer_support_history():
    data = request.get_json()
    data['sentiment'] = INVALID_SENTIMENT_SCORE
    with open('../data/customer_support_record.csv', mode='a', newline='') as file:
        cols = ['complaint_id','customer_id','date','transcript','main_concerns','is_repeating_issue','was_issue_resolved', 'sentiment']
        writer = csv.DictWriter(file, fieldnames=cols)
        writer.writerow(data)
    return {"customer_id": data['customer_id']}

if __name__ == '__main__':
    app.run(debug=True, port=5003)