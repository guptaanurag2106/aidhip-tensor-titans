import argparse
import csv
import json
import os

import pandas as pd
from param_mapper import cust_map
from utils import (
    load_product_list,
    mahalanobis_dist,
    send_request,
    weighted_vector_dist_passive,
)


def get_cust_info(customer_id: str) -> dict:
    cust_info = {"persona": {}, "transactions": [], "posts": [], "supports": []}
    output_dir = "./data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    customer_file = os.path.join(output_dir, "customer_profile.csv")
    transactions_file = os.path.join(output_dir, "customer_purchase.csv")
    social_media_file = os.path.join(output_dir, "social_media_record.csv")
    support_file = os.path.join(output_dir, "customer_support_record.csv")

    with open(customer_file, "r", newline="") as file:
        rows = csv.DictReader(file)
        for row in rows:
            if row["customer_id"] == customer_id:
                cust_info["persona"] = row
                break

    with open(transactions_file, "r", newline="") as file:
        rows = csv.DictReader(file)
        for row in rows:
            if row["customer_id"] == customer_id:
                cust_info["transactions"].append(row)

    with open(social_media_file, "r", newline="") as file:
        rows = csv.DictReader(file)
        for row in rows:
            if row["customer_id"] == customer_id:
                cust_info["posts"].append(row)

    with open(support_file, "r", newline="") as file:
        rows = csv.DictReader(file)
        for row in rows:
            if row["customer_id"] == customer_id:
                cust_info["supports"].append(row)

    return cust_info


def generate_cust_input_params(cust_info: dict) -> dict:
    prompt = f"""
    Given a customer of a popular U.S. bank with the following persona
    Persona: {cust_info["persona"]} (The list of loans, monthly spending, and balances are from older to newer)
    They have made the following transactions over the past 12 months
    Transactions: {cust_info["transactions"]}
    They have made the following social media posts
    Posts: {cust_info["posts"]}
    They have made the following support queries to the bank's support system
    Support Queries: {cust_info["supports"]}
    Analyze the data and give a json with the following properties

    chance_of_leaving: The chance of the customer leaving the bank (Type: Float, 0 means no chance of leaving, 0 negative sentiment support queries
                never said anything negative about the bank, 10 means will surely leave soon, Range: 0-10)
    profit_generated: The profits / money generated for the bank (Type: Float, 0 means generates loss for the bank, minimum(300) credit score unpayable loans, 
                      5 means average person (decent credit score, decent income, few loans (which they can pay based on their salary)
                      10 means generates huge profit for the bank full credit score(850), both as of current value, and of future expectations (talk of getting more money, positively promoting the bank etc.)
                    The income can go upto $1,00,000 for the wealthiest customer, so vary the profit_generated accordingly)
    risk_appetite: The risk appetite of the customer (Type: Float, 0 mean wants extremely safe investments or financial products with no chance of losing money even if
                it generates little to no money, 10 means wants highly risky investments which may generate a lot of money, but may lose a lot as well
    financial_acumen: Financial knowledge and experience of the Customer (Type: Float, 0 means has no knowledge and no previous experience with any financial field,
                10 means is very well versed in financial field, has a job in it, and has a history of making smart investments, good debts
    argument: Maximum 70 words proving why you chose this value, analyzing trends, identifying key moments, citing incidents etc.

    Return the customer parameters in a structured JSON format using the key mentioned after every field.
        """

    cust_input_params = {
        "churn_rate": 5,  # 0-10
        "profit_generated": 5,
        "risk_appetite": 5,
        "financial_acumen": 5,
        "argument": "",
    }

    response = send_request(prompt)

    if response.status_code == 200:
        response_data = response.json()
        response_text = response_data["choices"][0]["message"]["content"]

        try:
            response_text = response_text.strip().lstrip("```json").rstrip("```")

            response_data = json.loads(response_text)

            print(response_data)
            cust_input_params["churn_rate"] = response_data["chance_of_leaving"]
            cust_input_params["profit_generated"] = response_data["profit_generated"]
            cust_input_params["risk_appetite"] = response_data["risk_appetite"]
            cust_input_params["financial_acumen"] = response_data["financial_acumen"]
            cust_input_params["argument"] = response_data["argument"]
            return cust_input_params
        except:
            print("Could not parse JSON from response:", response_data)
            return cust_input_params
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return cust_input_params


def sort_products(cust_info: dict, products: list[dict]) -> str:
    prompt = f"""
    Given a customer of a popular U.S. bank with the following persona
    Persona: {cust_info["persona"]} (The list of loans, monthly spending, and balances are from older to newer)
    They have made the following transactions over the past 12 months
    Transactions: {cust_info["transactions"]}
    They have made the following social media posts
    Posts: {cust_info["posts"]}
    They have made the following support queries to the bank's support system
    Support Queries: {cust_info["supports"]}
    
    We have selected some financial products which we want to recommend to them, the list is as follows:
    Products: {products}
    Using the data, the customer's interest etc. sort the products list based on what they would want more.

    Output Content: 1 line: A comma separated string of product_id (example "PROD_1,PROD_54,PROD_2")
    Conent should only the list of product_id (as a comma separated string) of the sorted products in terms of customer interest highest to lowest,
    do not give any reasoning etc. just a comma separated string of product ids
        """
    response = send_request(prompt)

    if response.status_code == 200:
        response_data = response.json()
        response_text = response_data["choices"][0]["message"]["content"]

        response_data = response_text.split(",")
        response_data = ",".join([i.strip() for i in response_data])

        print(response_data)
        return response_data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return ",".join([i["product_id"] for i in products])


def main(customer_id: str):
    cust_info = get_cust_info(customer_id)

    print("Generating input params")
    cust_input_params = generate_cust_input_params(cust_info)
    cust_output_params = cust_map(cust_input_params)
    print("got params")

    cust_financial_products_path = "./data/financial_products.json"
    product_list = load_product_list(cust_financial_products_path)

    top_n_products = mahalanobis_dist(cust_output_params, product_list, 20)

    weights = {
        "risk_customer": 0.0,
        "value_customer": 0.2,
        "profit_margin": 0.2,
        "risk_bank": 0.0,
        "retention_value": 0.6,
    }  # weights should sum to 1
    top_n_passive_products = weighted_vector_dist_passive(
        cust_output_params, product_list, weights, 10
    )

    top_n_products = [
        {
            "product_id": product_list[i["index"]]["product_id"],
            "category": product_list[i["index"]]["category"],
            "subcategory": product_list[i["index"]]["subcategory"],
            "tier": product_list[i["index"]]["tier"],
            "name": product_list[i["index"]]["name"],
            "description": product_list[i["index"]]["description"],
            "details": product_list[i["index"]]["details"],
        }
        for i in top_n_products
    ]
    top_n_passive_products = [
        {
            "product_id": product_list[i["index"]]["product_id"],
            "category": product_list[i["index"]]["category"],
            "subcategory": product_list[i["index"]]["subcategory"],
            "tier": product_list[i["index"]]["tier"],
            "name": product_list[i["index"]]["name"],
            "description": product_list[i["index"]]["description"],
            "details": product_list[i["index"]]["details"],
        }
        for i in top_n_passive_products
    ]
    print("Got products")

    print("Sorting products")
    sorted_products = sort_products(cust_info, top_n_products)
    sorted_passive_products = sort_products(cust_info, top_n_passive_products)

    print("writing to csv")
    
    columns = [
        "input_params",
        "output_params",
        "top_n_products",
        "top_n_passive_products",
    ]
    new_values = [
        json.dumps(cust_input_params),
        json.dumps(cust_output_params),
        sorted_products,
        sorted_passive_products,
    ]
    df = pd.read_csv("./data/customer_profile.csv")
    df.loc[df["customer_id"] == customer_id, columns] = new_values
    df.to_csv("./data/customer_profile.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the magic AI for given customer id"
    )
    parser.add_argument(
        "--customer_id",
        type=str,
        default="CUST_1",
        required=False,
        help="Number of individual customers",
    )
    args = parser.parse_args()
    main(args.customer_id)
