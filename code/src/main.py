from param_mapper import cust_map
from utils import mahalanobis_dist, load_product_list, weighted_vector_dist_passive
import argparse
import os
import csv
from dotenv import load_dotenv
import json
import requests

load_dotenv()

OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")
OPEN_ROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-pro-exp-02-05:free"

headers = {
    "Authorization": f"Bearer {OPEN_ROUTER_KEY}",
    "Content-Type": "application/json",
}


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
    Support Queries: {cust_info["posts"]}
    Analyze the data and give a json with the following properties

    churn_rate: The chance of the customer leaving the bank (Type: Float, 0 means no chance of leaving, 10 means will surely leave soon)
    profit_generated: The profits / money generated for the bank (Type: Float, 0 means generates loss for the bank, 10 means generates huge profit for the bank)
    risk_appetite: The risk appetite of the customer (Type: Float, 0 mean wants very safe investments or financial products with no chance of losing money even if
                it generates little to no money, 10 means wants highly risky investments which may generate a lot of money, but may lose a lot as well
    financial_acumen: Financial knowledge and experience of the Customer (Type: Float, 0 means has no knowledge and no previous experience with any financial field,
                10 means is very well versed in financial field, maybe has a job in it, and has a history of making smart investments, good debts

    Return the customer parameters in a structured array of JSON format using the key mentioned after every field.
    Also give arguments for each of the parameters, with proof in the user data
        """
    payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}]}

    response = requests.post(OPEN_ROUTER_URL, headers=headers, data=json.dumps(payload))

    cust_input_params = {
        "churn_rate": 5,  # 0-10
        "profit_generated": 5,
        "risk_appetite": 5,
        "financial_acumen": 5,
    }

    if response.status_code == 200:
        response_data = response.json()
        response_text = response_data["choices"][0]["message"]["content"]

        try:
            response_text = response_text.strip().lstrip("```json").rstrip("```")

            response_data = json.loads(response_text)

            print(response_data)
            cust_input_params["churn_rate"] = response_data["churn_rate"]
            cust_input_params["profit_generated"] = response_data["profit_generated"]
            cust_input_params["risk_appetite"] = response_data["risk_appetite"]
            cust_input_params["financial_acumen"] = response_data["financial_acumen"]
            return cust_input_params
        except:
            print("Could not parse JSON from response:", response_data)
            return cust_input_params
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return cust_input_params


def sort_products(cust_info: dict, products: list[dict]) -> list[dict]:
    prompt = f"""
    Given a customer of a popular U.S. bank with the following persona
    Persona: {cust_info["persona"]} (The list of loans, monthly spending, and balances are from older to newer)
    They have made the following transactions over the past 12 months
    Transactions: {cust_info["transactions"]}
    They have made the following social media posts
    Posts: {cust_info["posts"]}
    They have made the following support queries to the bank's support system
    Support Queries: {cust_info["posts"]}
    
    We have selected some financial products which we want to recommend to them,
    the list is as follows:
    Products: {products}
    Analyze the data, the customer's interest etc. and sort the products list based on what they would want more.

    Return only the list of product_id (as a comma separated string) of the sorted products in terms of customer interest highest to lowest,
    do not return anything else (analysis/description etc.) just a comma separated string of product ids
        """
    payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}]}

    response = requests.post(OPEN_ROUTER_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        response_text = response_data["choices"][0]["message"]["content"]

        response_data = response_text.split(",")
        response_data = [i.strip() for i in response_data]

        print(response_data)
        return response_data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []


def main(customer_id: str) -> tuple[list[dict], list[dict]]:
    cust_info = get_cust_info(customer_id)

    cust_input_params = generate_cust_input_params(cust_info)
    cust_output_params = cust_map(cust_input_params)

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
    top_n_passive_products = [product_list[i["index"]] for i in top_n_passive_products]

    sorted_products = sort_products(cust_info, top_n_products)
    sorted_passive_products = sort_products(cust_info, top_n_passive_products)

    return sorted_products, sorted_passive_products


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
