import argparse
import csv
import json
import os
import random

import requests
from dotenv import load_dotenv
from prompt_list import (
    create_customer_complaint_prompt,
    create_customer_persona_prompt,
    create_social_media_prompt,
    create_transaction_history_prompt,
)

load_dotenv()

OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")
OPEN_ROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-pro-exp-02-05:free"

headers = {
    "Authorization": f"Bearer {OPEN_ROUTER_KEY}",
    "Content-Type": "application/json",
}


def request_parse_ret(prompt, count):
    payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}]}

    response = requests.post(OPEN_ROUTER_URL, headers=headers, data=json.dumps(payload))
    final_response = []

    if response.status_code == 200:
        response_data = response.json()

        try:
            response_text = response_data["choices"][0]["message"]["content"]
            response_text = response_text.strip().lstrip("```json").rstrip("```")

            response_data = json.loads(response_text)
            response_json = json.dumps(response_data, indent=2)

            for i in range(count):
                try:
                    start_idx = response_json[i].find("{")
                    end_idx = response_json[i].rfind("}") + 1
                    if start_idx != -1 and end_idx != -1:
                        r = json.loads(response_json[i][start_idx:end_idx])
                        final_response.append(r)
                    else:
                        return json.loads(response_json)
                except json.JSONDecodeError:
                    print(f"Could not parse JSON from response[{i}]:", response_json[i])
                    continue
        except:
            print("Could not parse JSON from response:", response_data)
            return None
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

    with open(customer_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "customer_id",
                "age",
                "gender",
                "income",
                "education",
                "is_married",
                "num_of_children",
                "location",
                "job",
                "goals",
                "credit_score",
                "preferred_payment_method",
                "avg_balance",
                "loan_count",
                "total_loan_amt",
                "avg_monthly_spending",
                "main_purchase_cat",
                "support_interaction_count",
                "satisfaction",
            ]
        )

    with open(transactions_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "transaction_id",
                "customer_id",
                "date",
                "platform",
                "payment_method",
                "amt",
                "location",
                "item_category",
                "item_sub_category",
                "item_brand",
            ]
        )

    with open(social_media_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "post_id",
                "customer_id",
                "date",
                "platform",
                "image_url",
                "text_content",
                "influencers_followed",
                "topics_of_interest",
                "feedback_on_financial_products",
                "sentiment_score",
                "engagement_level",
                "brands_liked",
            ]
        )

    with open(support_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "complaint_id",
                "customer_id",
                "date",
                "transcript",
                "main_concerns",
                "is_repeating_issue",
                "was_issue_resolved",
                "sentiment",
            ]
        )

    # personas = generate_customer_persona(args.customer_count)
    print("Generating Customer Data")
    personas = request_parse_ret(
        create_customer_persona_prompt(args.customer_count), args.customer_count
    )
    if not personas:
        return

    customer_id = 1
    transaction_id = 1
    complaint_id = 1
    post_id = 1
    for customer_id in range(1, args.customer_count + 1):
        persona = personas[customer_id - 1]
        numbers = [random.random() for _ in range(10)]
        avg = sum(numbers) / len(numbers)
        result = 7 + (avg - 0.5) * 6
        persona["satisfaction"] = max(0, min(10, result))

        with open(customer_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    f"CUST_{customer_id}",
                    persona.get("age", ""),
                    persona.get("gender", ""),
                    persona.get("income", ""),
                    persona.get("education", ""),
                    persona.get("is_married", ""),
                    persona.get("num_of_children", ""),
                    persona.get("location", ""),
                    persona.get("job", ""),
                    persona.get("goals", ""),
                    persona.get("credit_score", ""),
                    persona.get("preferred_payment_method", ""),
                    persona.get("avg_balance", ""),
                    persona.get("loan_count", ""),
                    persona.get("total_loan_amt", ""),
                    persona.get("avg_monthly_spending", ""),
                    persona.get("main_purchase_cat", ""),
                    persona.get("support_interaction_count", ""),
                    persona.get("satisfaction", ""),
                ]
            )

        print(f"Generating Transaction Data {customer_id}/{args.customer_count}")
        transactions = request_parse_ret(
            create_transaction_history_prompt(persona, args.max_purchase_count),
            args.max_purchase_count,
        )
        if transactions:
            for transaction in transactions:
                with open(transactions_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [
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
                        ]
                    )
                    transaction_id += 1

        print(f"Generating Complaint Data {customer_id}/{args.customer_count}")
        complaints = request_parse_ret(
            create_customer_complaint_prompt(
                persona, persona.get("support_interaction_count", 5)
            ),
            persona.get("support_interaction_count", 5),
        )
        if complaints:
            for complaint in complaints:
                with open(support_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [
                            f"SPRT_{complaint_id}",
                            f"CUST_{customer_id}",
                            complaint.get("date", ""),
                            complaint.get("transcript", ""),
                            complaint.get("main_concerns", ""),
                            complaint.get("is_repeating_issue", ""),
                            complaint.get("was_issue_resolved", ""),
                            complaint.get("sentiment", ""),
                        ]
                    )
                    complaint_id += 1

        print(f"Generating Posts Data {customer_id}/{args.customer_count}")
        posts = request_parse_ret(
            create_social_media_prompt(persona, args.max_post), args.max_post
        )
        if posts:
            for post in posts:
                with open(social_media_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [
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
                        ]
                    )
                    post_id += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate CSV files for customer data."
    )
    parser.add_argument(
        "--customer_count",
        type=int,
        default=5,
        required=False,
        help="Number of individual customers",
    )
    parser.add_argument(
        "--corporate_count",
        type=int,
        default=5,
        required=False,
        help="Number of corporate customers",
    )
    parser.add_argument(
        "--max_post",
        type=int,
        default=20,
        required=False,
        help="Max number of social media posts per person",
    )
    parser.add_argument(
        "--max_purchase_count",
        type=int,
        default=25,
        required=False,
        help="Max number of purchase history per person",
    )
    args = parser.parse_args()
    main(args)
