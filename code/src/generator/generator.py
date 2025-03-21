import json
import os
import argparse
import csv
import random

import requests
from dotenv import load_dotenv

load_dotenv()

OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")
OPEN_ROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-pro-exp-02-05:free"

headers = {
    "Authorization": f"Bearer {OPEN_ROUTER_KEY}",
    "Content-Type": "application/json"
}

def create_customer_persona_prompt(cust_count):
    return  f"""
        Create {cust_count} detailed bank customer persona with the following attributes and only the following attributes:
        - age: Age (Range: Integer, typically 18-100)
        - gender: Gender (Type: String, Options: Male/Female/Other)
        - income: Income (Range: Integer, between 10,000 and 1,000,000)
        - education: Education (Type: String, Options: Primary/Secondary/Graduate)
        - is_married: Is Married (Type: Boolean)
        - num_of_children: Number of Children (Range: Integer, between 0 and 5)
        - job: Job/Career (Type: String)
        - credit_score: Credit Score (Range: Integer, typically 300-850)
        - preferred_payment_method: Preferred Payment Method (Type: String, Options: Credit Card/Debit Card/Cash/Online)
        - location: Location (U.S.A. State)
        - avg_balance: Average Past 12 Month Bank Balance (Type: Float/Integer)
        - loan_count: Number of Lifetime Loans (Range: Integer, 0 and above)
        - total_loan_amt: Total Loan Amount (Range: Float/Integer)
        - avg_monthly_spending: Average Monthly Spending (Type: Float/Integer)
        - main_purchase_cat: Main Purchase Categories (Comma Separated String)
        - support_interaction_count: Number of Lifetime Support Interactions (Range: Integer)
        The data should be congruent with itself and be representative of average U.S. population in the demographic
        Return the persona in a structured array of JSON format using the key mentioned after every field.
        """
    

# def generate_customer_persona(cust_count):
#     prompt = f"""
#     Create {cust_count} detailed bank customer persona with the following attributes and only the following attributes:
#     - age: Age (Range: Integer, typically 18-100)
#     - gender: Gender (Type: String, Options: Male/Female/Other)
#     - income: Income (Range: Integer, between 10,000 and 1,000,000)
#     - education: Education (Type: String, Options: Primary/Secondary/Graduate)
#     - is_married: Is Married (Type: Boolean)
#     - num_of_children: Number of Children (Range: Integer, between 0 and 5)
#     - job: Job/Career (Type: String)
#     - credit_score: Credit Score (Range: Integer, typically 300-850)
#     - preferred_payment_method: Preferred Payment Method (Type: String, Options: Credit Card/Debit Card/Cash/Online)
#     - location: Location (U.S.A. State)
#     - avg_balance: Average Past 12 Month Bank Balance (Type: Float/Integer)
#     - loan_count: Number of Lifetime Loans (Range: Integer, 0 and above)
#     - total_loan_amt: Total Loan Amount (Range: Float/Integer)
#     - avg_monthly_spending: Average Monthly Spending (Type: Float/Integer)
#     - main_purchase_cat: Main Purchase Categories (Comma Separated String)
#     - support_interaction_count: Number of Lifetime Support Interactions (Range: Integer)
#     The data should be congruent with itself and be representative of average U.S. population in the demographic
#     Return the persona in a structured array of JSON format using the key mentioned after every field.
#     """
#     
#     payload = {
#         "model":MODEL,
#         "messages": [
#             {"role": "user", "content": prompt}
#         ]
#     }
#     
#     response = requests.post(OPEN_ROUTER_URL, headers=headers, data=json.dumps(payload))
#     personas = []
#     
#     if response.status_code == 200:
#         response_data = response.json()
#         persona_text = response_data["choices"][0]["message"]["content"]
#         persona_text = persona_text.strip().lstrip('```json').rstrip('```')
#         response_data = json.loads(persona_text)
#
#         persona = json.dumps(response_data, indent=2)
#         print(persona)
#         
#         for i in range(cust_count):
#             try:
#                 start_idx = persona[i].find('{')
#                 end_idx = persona[i].rfind('}') + 1
#                 if start_idx != -1 and end_idx != -1:
#                     persona_json = json.loads(persona[i][start_idx:end_idx])
#                     personas.append(persona_json)
#                 else:
#                     return json.loads(persona)
#             except json.JSONDecodeError:
#                 print("Could not parse JSON from response")
#                 print(persona[i])
#                 continue
#     else:
#         print(f"Error: {response.status_code}")
#         print(response.text)
#         return None

def create_transaction_history_prompt(persona, num_transactions):
    return f"""
    Generate between 1 and {num_transactions} realistic bank transactions for the following customer:
    Age: {persona["age"]}
    Gender: {persona["gender"]}
    Income: {persona["income"]}
    Education: {persona["education"]}
    Is Married: {persona["is_married"]}
    Number of Children: {persona["num_of_children"]}
    Job/Career: {persona["job"]}
    Credit Score: {persona["credit_score"]}
    Preferred Payment Method: {persona["preferred_payment_method"]}
    Location: {persona["location"]}
    Average Past 12 Month Bank Balance: {persona["avg_balance"]}
    Number of Lifetime Loans: {persona["loan_count"]}
    Total Loan Amount: {persona["total_loan_amt"]}
    Average Monthly Spending: {persona["avg_monthly_spending"]}
    Main Purchase Categories: {persona["main_purchase_cat"]}
    Number of Lifetime Support Interactions: {persona["support_interaction_count"]}
    
    From these info about the customer using their preferred_payment_method (not always the same),
    there income, categories generate the following data (It can have some outliers but most should follow the customer info),
    Also make sure the Average Monthly Spending matches with the transactions created
    Each transaction should include these and only these attributes:

    date: Date (Format: DD/MM/YYYY should be within last year)
    platform: Platform (Type: String, Options: Amazon/Online/Offline etc.)
    payment_method: Payment Method (Options: Credit Card/Debit Card/Cash/Venmo/Zelle etc.)
    amt: Amt (Type: Float, Example: 100.00)
    location: Location (Type: String, Example: State)
    item_category: Item Category (Type: String, Example: Electronics, Apparel, etc.)
    item_sub_category: Item Sub Category (Type: String, Example: Laptop, Shoes, etc.)
    item_brand: Item Brand (Type: String, Example: Apple, Nike, etc.)
    
    Return the transactions as a JSON array.
    """

def create_customer_complaint_prompt(persona, num_complaints):
    if num_complaints == 0:
        return []
    
    return f"""
    Generate {num_complaints} realistic customer support complaints to a popular U.S.A bank for the following bank customer:
    Age: {persona["age"]}
    Gender: {persona["gender"]}
    Income: {persona["income"]}
    Education: {persona["education"]}
    Is Married: {persona["is_married"]}
    Number of Children: {persona["num_of_children"]}
    Job/Career: {persona["job"]}
    Credit Score: {persona["credit_score"]}
    Preferred Payment Method: {persona["preferred_payment_method"]}
    Location: {persona["location"]}
    Average Past 12 Month Bank Balance: {persona["avg_balance"]}
    Number of Lifetime Loans: {persona["loan_count"]}
    Total Loan Amount: {persona["total_loan_amt"]}
    Average Monthly Spending: {persona["avg_monthly_spending"]}
    Main Purchase Categories: {persona["main_purchase_cat"]}
    Number of Lifetime Support Interactions: {persona["support_interaction_count"]}
    Satisfaction with bank: {persona["satisfaction"]}/10
    
    Each complaint should include the following and only these attributes:
    date: Date (Format: DD/MM/YYYY should be in past 1 year)
    transcript: Transcript (Type: String, Max: 150 words, Text: Full transcript of the conversation)
    main_concerns: Main Concerns (Type: String, Example: "Billing issue", "Technical support")
    is_repeating_issue: Is Repeating Issue (Type: Boolean, True/False)
    was_issue_resolved: Was Issue Resolved (Type: Boolean, True/False)
    sentiment: Sentiment (Type: Double, Options: -1 to 1)
    
    Return the complaints as a JSON array.
    """

def create_social_media_prompt(persona, num_posts):
   sentiment = "mostly positive" if persona["satisfaction"] >= 7 else "mixed" if persona["satisfaction"] >= 4 else "mostly negative"
    
   return f"""
    Generate maximim of {num_posts} realistic social media posts (tweets) for the following bank customer:
    
    Age: {persona["age"]}
    Gender: {persona["gender"]}
    Income: {persona["income"]}
    Education: {persona["education"]}
    Is Married: {persona["is_married"]}
    Number of Children: {persona["num_of_children"]}
    Job/Career: {persona["job"]}
    Credit Score: {persona["credit_score"]}
    Preferred Payment Method: {persona["preferred_payment_method"]}
    Location: {persona["location"]}
    Average Past 12 Month Bank Balance: {persona["avg_balance"]}
    Number of Lifetime Loans: {persona["loan_count"]}
    Total Loan Amount: {persona["total_loan_amt"]}
    Average Monthly Spending: {persona["avg_monthly_spending"]}
    Main Purchase Categories: {persona["main_purchase_cat"]}
    Number of Lifetime Support Interactions: {persona["support_interaction_count"]}
    Satisfaction with bank: {persona["satisfaction"]}/10
    
    The posts should be a mix of general life posts and occasionally banking-related posts.
    The banking-related sentiment should be {sentiment} based on their satisfaction level.
    Each post should include the following and only these attributes:

    date: Date (Format: DD/MM/YY should be in past 1 year)
    platform: Platform (Options: 'Online', 'Offline')
    image_url: Image URL (Type: String, Example: 'https://example.com/images/abcd1234.jpg')
    text_content: Text Content (Type: String, Example: 'This is some text content about a product or service.')
    influencers_followed: Influencers Followed (Range: Integer, 0-10, Example: 5)
    topics_of_interest: Topics of Interest (Type: List of Strings, Example: ['Technology', 'Sports', 'Finance'])
    feedback_on_financial_products: Feedback on Financial Products (Options: 'Positive', 'Negative', 'Neutral')
    sentiment_score: Sentiment Score (Range: Float, 0.0 to 10.0, Example: 7.4)
    engagement_level: Engagement Level (Range: Float, 0.0 to 10.0, Example: 6.2)
    brands_liked: Brands Liked (Type: List of Strings, Example: ['Nike', 'Apple', 'Tesla'])
    
    Return the posts as a JSON array.
    """

def request_parse_ret(prompt, count):
    
    payload = {
        "model":MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post(OPEN_ROUTER_URL, headers=headers, data=json.dumps(payload))
    final_response = []
    
    if response.status_code == 200:
        response_data = response.json()
        response_text = response_data["choices"][0]["message"]["content"]
        response_text = response_text.strip().lstrip('```json').rstrip('```')
        response_data = json.loads(response_text)

        response_json = json.dumps(response_data, indent=2)
        print(response_json)
        
        for i in range(count):
            try:
                start_idx = response_json[i].find('{')
                end_idx = response_json[i].rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    r = json.loads(response_json[i][start_idx:end_idx])
                    final_response.append(r)
                else:
                    return json.loads(response_json)
            except json.JSONDecodeError:
                print("Could not parse JSON from response")
                continue
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

    return final_response


def main(args):
    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    customer_file = os.path.join(output_dir, "customer_profile.csv")
    transactions_file = os.path.join(output_dir, "customer_purchase.csv")
    social_media_file = os.path.join(output_dir, "social_media_record.csv")
    support_file = os.path.join(output_dir, "customer_support_record.csv")

    with open(customer_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['customer_id', 'age', 'gender', 'income', 'education', 
                         'is_married', 'num_of_children', 'job', 'credit_score', 
                         'preferred_payment_method', 'location', 'avg_balance', 'loan_count', 
                         'total_loan_amt', 'avg_monthly_spending', 'main_purchase_cat', 'support_interaction_count', 'satisfaction'])

    with open(transactions_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['transaction_id', 'customer_id', 'date', 'platform', 'payment_method', 'amt',
                         'location', 'item_category', 'item_sub_category', 'item_brand'])

    with open(social_media_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['post_id', 'customer_id', 'date','platform', 'image_url', 'text_content', 'influencers_followed',
                         'topics_of_interest', 'feedback_on_financial_products', 'sentiment_score', 'engagement_level', 'brands_liked'])

    with open(support_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['complaint_id', 'customer_id', 'date', 'transcript', 'main_concerns', 'is_repeating_issue', 'was_issue_resolved', 'sentiment'])


    # personas = generate_customer_persona(args.customer_count)
    print("Generating Customer Data")
    personas = request_parse_ret(create_customer_persona_prompt(args.customer_count), args.customer_count)
    if not personas:
        return

    customer_id = 1
    for customer_id in range(1, args.customer_count + 1):
        persona = personas[customer_id-1]
        numbers = [random.random() for _ in range(10)]
        avg = sum(numbers) / len(numbers)
        result = 7 + (avg - 0.5) * 6
        persona["satisfaction"] = max(0, min(10, result))
    
        with open(customer_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                f"CUST_{customer_id}",
                persona.get('age', ""),
                persona.get('gender', ""),
                persona.get('income', ""),
                persona.get('education',  ""),
                persona.get('is_married', ""),
                persona.get('num_of_children', ""),
                persona.get('job', ""),
                persona.get('credit_score',  ""),
                persona.get('preferred_payment_method', ""),
                persona.get('location', ""),
                persona.get('avg_balance', ""),
                persona.get('loan_count', ""),
                persona.get('total_loan_amt', ""),
                persona.get('avg_monthly_spending', ""),
                persona.get('main_purchase_cat', ""),
                persona.get('support_interaction_count', ""),
                persona.get('satisfaction', ""),
            ])

        transaction_id = 1
        print(f"Generating Transaction Data {customer_id}/{args.customer_count}")
        transactions = request_parse_ret(create_transaction_history_prompt(persona, args.max_purchase_count), args.max_purchase_count)
        if transactions:
            for transaction in transactions:
                with open(transactions_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        f"TXN_{transaction_id}",
                        f"CUST_{customer_id}",
                        transaction.get("date", ""),
                        transaction.get("platform", ""),
                        transaction.get("payment_method", ""),
                        transaction.get("amt", ""),
                        transaction.get("location", ""),
                        transaction.get("item_category", ""),
                        transaction.get("item_sub_category", ""),
                        transaction.get("item_brand", ""),
                    ])
                    transaction_id += 1

        complaint_id = 1
        print(f"Generating Complaint Data {customer_id}/{args.customer_count}")
        complaints = request_parse_ret(create_customer_complaint_prompt(persona, persona.get("support_interaction_count", 5)), persona.get("support_interaction_count", 5))
        if complaints:
            for complaint in complaints:
                with open(support_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        f"SPRT_{complaint_id}",
                        f"CUST_{customer_id}",
                        complaint.get("date", ""),
                        complaint.get("transcript", ""),
                        complaint.get("main_concerns", ""),
                        complaint.get("is_repeating_issue", ""),
                        complaint.get("was_issue_resolved", ""),
                        complaint.get("sentiment", ""),
                    ])
                    complaint_id += 1

        post_id = 1
        print(f"Generating Posts Data {customer_id}/{args.customer_count}")
        posts = request_parse_ret(create_social_media_prompt(persona, args.max_post), args.max_post)
        if posts:
            for post in posts:
                with open(social_media_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        f"POST_{post_id}",
                        f"CUST_{customer_id}",
                        post.get("date", ""),
                        post.get("platform", ""),
                        post.get("image_url", ""),
                        post.get("text_content", ""),
                        post.get("influencers_followed", ""),
                        post.get("topics_of_interest", ""),
                        post.get("feedback_on_financial_products", ""),
                        post.get("sentiment_score", ""),
                        post.get("engagement_level", ""),
                        post.get("brands_liked", ""),
                    ])
                    post_id += 1



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate CSV files for customer data.")
    parser.add_argument("--customer_count", type=int, default=5,required=False, help="Number of individual customers")
    parser.add_argument("--corporate_count", type=int, default=5, required=False, help="Number of corporate customers")
    parser.add_argument("--max_post", type=int, default=20, required=False, help="Max number of social media posts per person")
    parser.add_argument("--max_purchase_count", type=int, default=20, required=False, help="Max number of purchase history per person")
    args = parser.parse_args()
    main(args)
