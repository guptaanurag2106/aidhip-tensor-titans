import argparse
import csv
import json
import os
import random
import requests
from dotenv import load_dotenv
from org_prompt_list import (
    create_org_persona_prompt,
    create_org_support_prompt,
    create_org_social_media_prompt,
    create_org_transaction_history_prompt,
)

load_dotenv(".env.local")

OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")
OPEN_ROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-pro-exp-02-05:free"

MIN_TRANSACTIONS = 3
MIN_SUPPORT_TICKETS = 2
MIN_SOCIAL_POSTS = 2

headers = {
    "Authorization": f"Bearer {OPEN_ROUTER_KEY}",
    "Content-Type": "application/json",
}

def request_parse_ret(prompt, count, max_retries=3):
    final_response = []
    
    for retry in range(max_retries):
        payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}]}
        response = requests.post(OPEN_ROUTER_URL, headers=headers, json=payload)  

        if response.status_code == 200:
            response_data = response.json()
            response_text = ""
            
            try:
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    if "message" in response_data["choices"][0] and "content" in response_data["choices"][0]["message"]:
                        response_text = response_data["choices"][0]["message"]["content"].strip()
                        
                        if "```json" in response_text:
                            json_start = response_text.find("```json") + 7
                            json_end = response_text.rfind("```")
                            if json_end > json_start:
                                response_text = response_text[json_start:json_end].strip()
                        
                        if not response_text.startswith("{") and not response_text.startswith("["):
                            response_text = "[" + response_text + "]"
                        
                        parsed_data = json.loads(response_text)
                        
                        if isinstance(parsed_data, list):
                            for item in parsed_data[:count]:
                                if isinstance(item, dict):
                                    final_response.append(item)
                        elif isinstance(parsed_data, dict):
                            final_response.append(parsed_data)
                else:
                    if "text" in response_data:
                        response_text = response_data["text"].strip()
                    elif "response" in response_data:
                        response_text = response_data["response"].strip()
            except (KeyError, json.JSONDecodeError):                
                if response_text:
                    try:
                        fixed_text = response_text.replace("'", '"')
                        parsed_data = json.loads(fixed_text)
                        
                        if isinstance(parsed_data, list):
                            for item in parsed_data[:count]:
                                if isinstance(item, dict):
                                    final_response.append(item)
                        elif isinstance(parsed_data, dict):
                            final_response.append(parsed_data)
                    except json.JSONDecodeError:
                        pass
        
        if len(final_response) >= min(3, count):
            break
        
        if retry < max_retries - 1:
            import time
            time.sleep(1)
    
    return final_response


def generate_fallback_data(data_type, org_id, persona, count):
    """Generate fallback data if API fails to return results"""
    result = []
    
    if data_type == "transaction":
        for i in range(count):
            categories = ["Office Supplies", "Software", "Marketing", "Travel", "Hardware"]
            vendors = ["Amazon", "Microsoft", "Google", "Office Depot", "Dell"]
            
            result.append({
                "date": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                "platform": random.choice(["Web", "Mobile", "In-Person"]),
                "payment_method": random.choice(["Credit Card", "ACH", "Wire Transfer"]),
                "amount": f"${random.randint(100, 5000)}.{random.randint(0, 99):02d}",
                "location": persona.get("location", "Unknown"),
                "expense_category": random.choice(categories),
                "expense_sub_category": f"Sub-{random.choice(categories)}",
                "vendor": random.choice(vendors),
                "transaction_type": random.choice(["Purchase", "Subscription", "Refund"])
            })
            
    elif data_type == "support":
        for i in range(count):
            issues = ["Login Issue", "Payment Problem", "Account Access", "Technical Error"]
            
            result.append({
                "date": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                "transcript": f"Customer reported {random.choice(issues)}. Agent resolved the issue.",
                "issue_type": random.choice(issues),
                "priority": random.choice(["Low", "Medium", "High"]),
                "is_repeating_issue": random.choice(["Yes", "No"]),
                "was_issue_resolved": random.choice(["Yes", "No"]),
                "resolution_time": f"{random.randint(1, 24)} hours",
                "sentiment": random.choice(["Positive", "Neutral", "Negative"])
            })
            
    elif data_type == "social":
        for i in range(count):
            platforms = ["Twitter", "LinkedIn", "Facebook", "Instagram"]
            
            result.append({
                "date": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                "platform": random.choice(platforms),
                "image_url": "",
                "text_content": f"{persona.get('company_name', 'Our company')} is excited to announce new developments!",
                "topics_of_interest": random.choice(["Finance", "Technology", "Business", "Innovation"]),
                "feedback_on_financial_services": "",
                "sentiment_score": str(round(random.uniform(0, 1), 2)),
                "engagement_level": str(random.randint(1, 100)),
                "partners_mentioned": "",
                "post_type": random.choice(["Announcement", "Update", "News", "Product"])
            })
    
    return result


def main(args):
    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    org_file = os.path.join(output_dir, "org_profile.csv")
    transactions_file = os.path.join(output_dir, "org_purchase.csv")
    social_media_file = os.path.join(output_dir, "org_social_media_record.csv")
    support_file = os.path.join(output_dir, "org_support_record.csv")

    with open(org_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "org_id", "company_name", "industry", "size", "annual_revenue", 
            "years_in_business", "location", "business_model", "growth_stage", 
            "risk_tolerance", "credit_rating", "preferred_payment_method", 
            "avg_account_balance", "loan_count", "total_loan_amt", 
            "avg_monthly_spending", "main_expense_categories", 
            "support_interaction_count", "satisfaction"
        ])

    with open(transactions_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "transaction_id", "org_id", "date", "platform", "payment_method", 
            "amount", "location", "expense_category", "expense_sub_category", 
            "vendor", "transaction_type"
        ])

    with open(social_media_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "post_id", "org_id", "date", "platform", "image_url", "text_content", 
            "topics_of_interest", "feedback_on_financial_services", 
            "sentiment_score", "engagement_level", "partners_mentioned", "post_type"
        ])

    with open(support_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ticket_id", "org_id", "date", "transcript", "issue_type", "priority", 
            "is_repeating_issue", "was_issue_resolved", "resolution_time", "sentiment"
        ])

    org_prompt = create_org_persona_prompt(args.org_count)
    org_personas = request_parse_ret(org_prompt, args.org_count)
    
    
    if not org_personas or len(org_personas) < args.org_count:        
        for i in range(len(org_personas) if org_personas else 0, args.org_count):
            industries = ["Technology", "Finance", "Healthcare", "Retail", "Manufacturing"]
            org_personas.append({
                "company_name": f"Company {i+1}",
                "industry": random.choice(industries),
                "size": random.choice(["Small", "Medium", "Large"]),
                "annual_revenue": f"${random.randint(1, 100)}M",
                "years_in_business": str(random.randint(1, 20)),
                "location": "United States",
                "business_model": random.choice(["B2B", "B2C", "Hybrid"]),
                "growth_stage": random.choice(["Startup", "Growth", "Mature"]),
                "risk_tolerance": random.choice(["Low", "Medium", "High"]),
                "credit_rating": random.choice(["A", "B", "C"]),
                "preferred_payment_method": random.choice(["Credit Card", "ACH", "Wire"]),
                "avg_account_balance": f"${random.randint(10000, 1000000)}",
                "loan_count": str(random.randint(0, 5)),
                "total_loan_amt": f"${random.randint(0, 500000)}",
                "avg_monthly_spending": f"${random.randint(5000, 50000)}",
                "main_expense_categories": random.choice(["Technology", "Marketing", "Operations"]),
                "support_interaction_count": str(random.randint(1, 10))
            })
    
    transaction_id = 1
    ticket_id = 1
    post_id = 1
    
    for org_id in range(1, args.org_count + 1):
        if org_id > len(org_personas):
            break
            
        persona = org_personas[org_id - 1]
        
        if not isinstance(persona, dict):
            continue
       
        numbers = [random.random() for _ in range(10)]
        avg = sum(numbers) / len(numbers)
        result = 7 + (avg - 0.5) * 6
        persona["satisfaction"] = max(0, min(10, result))

        with open(org_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                f"ORG_{org_id}",
                persona.get("company_name", ""),
                persona.get("industry", ""),
                persona.get("size", ""),
                persona.get("annual_revenue", ""),
                persona.get("years_in_business", ""),
                persona.get("location", ""),
                persona.get("business_model", ""),
                persona.get("growth_stage", ""),
                persona.get("risk_tolerance", ""),
                persona.get("credit_rating", ""),
                persona.get("preferred_payment_method", ""),
                persona.get("avg_account_balance", ""),
                persona.get("loan_count", ""),
                persona.get("total_loan_amt", ""),
                persona.get("avg_monthly_spending", ""),
                persona.get("main_expense_categories", ""),
                persona.get("support_interaction_count", ""),
                persona.get("satisfaction", "")
            ])

        transactions = request_parse_ret(
            create_org_transaction_history_prompt(persona, args.max_purchase_count),
            args.max_purchase_count
        )
        
        if not transactions or len(transactions) < MIN_TRANSACTIONS:
            fallback_count = MIN_TRANSACTIONS if not transactions else (MIN_TRANSACTIONS - len(transactions))
            fallback_transactions = generate_fallback_data("transaction", org_id, persona, fallback_count)
            if transactions:
                transactions.extend(fallback_transactions)
            else:
                transactions = fallback_transactions
        
        for transaction in transactions:
            if not isinstance(transaction, dict):
                continue
                
            with open(transactions_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    f"TXN_{transaction_id}",
                    f"ORG_{org_id}",
                    transaction.get("date", ""),
                    transaction.get("platform", ""),
                    transaction.get("payment_method", ""),
                    transaction.get("amount", ""),
                    transaction.get("location", ""),
                    transaction.get("expense_category", ""),
                    transaction.get("expense_sub_category", ""),
                    transaction.get("vendor", ""),
                    transaction.get("transaction_type", "")
                ])
                transaction_id += 1

        support_count = max(MIN_SUPPORT_TICKETS, int(persona.get("support_interaction_count", 5)))
        support_tickets = request_parse_ret(
            create_org_support_prompt(persona, support_count),
            support_count
        )
        
        
        if not support_tickets or len(support_tickets) < MIN_SUPPORT_TICKETS:
            fallback_count = MIN_SUPPORT_TICKETS if not support_tickets else (MIN_SUPPORT_TICKETS - len(support_tickets))
            fallback_tickets = generate_fallback_data("support", org_id, persona, fallback_count)
            if support_tickets:
                support_tickets.extend(fallback_tickets)
            else:
                support_tickets = fallback_tickets
        
        for ticket in support_tickets:
            if not isinstance(ticket, dict):
                continue
                
            with open(support_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    f"TICK_{ticket_id}",
                    f"ORG_{org_id}",
                    ticket.get("date", ""),
                    ticket.get("transcript", ""),
                    ticket.get("issue_type", ""),
                    ticket.get("priority", ""),
                    ticket.get("is_repeating_issue", ""),
                    ticket.get("was_issue_resolved", ""),
                    ticket.get("resolution_time", ""),
                    ticket.get("sentiment", "")
                ])
                ticket_id += 1

        
        posts = request_parse_ret(
            create_org_social_media_prompt(persona, args.max_post), 
            args.max_post
        )
        
        if not posts or len(posts) < MIN_SOCIAL_POSTS:
            fallback_count = MIN_SOCIAL_POSTS if not posts else (MIN_SOCIAL_POSTS - len(posts))
            fallback_posts = generate_fallback_data("social", org_id, persona, fallback_count)
            if posts:
                posts.extend(fallback_posts)
            else:
                posts = fallback_posts
        
        for post in posts:
            if not isinstance(post, dict):
                continue
                
            with open(social_media_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    f"POST_{post_id}",
                    f"ORG_{org_id}",
                    post.get("date", ""),
                    post.get("platform", ""),
                    post.get("image_url", ""),
                    post.get("text_content", ""),                    
                    post.get("topics_of_interest", ""),
                    post.get("feedback_on_financial_services", ""),
                    post.get("sentiment_score", ""),
                    post.get("engagement_level", ""),
                    post.get("partners_mentioned", ""),
                    post.get("post_type", "")
                ])
                post_id += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate CSV files for organization data."
    )
    parser.add_argument(
        "--org_count",
        type=int,
        default=5,
        required=False,
        help="Number of organizations"
    )
    parser.add_argument(
        "--max_post",
        type=int,
        default=15,
        required=False,
        help="Max number of social media posts per organization"
    )
    parser.add_argument(
        "--max_purchase_count",
        type=int,
        default=20,
        required=False,
        help="Max number of purchase/expense records per organization"
    )
    args = parser.parse_args()
    main(args)
