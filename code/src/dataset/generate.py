import argparse
import random
import numpy as np
from faker import Faker
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description="Generate CSV files for customer data.")
    parser.add_argument("--customer_count", type=int, required=True, help="Number of individual customers")
    parser.add_argument("--corporate_count", type=int, required=True, help="Number of corporate customers")
    parser.add_argument("--seed", type=int, default=42, help="Seed for random number generation")
    return parser.parse_args()

# Parse arguments and set seeds for reproducibility
args = parse_args()
random.seed(args.seed)
np.random.seed(args.seed)
fake = Faker()
Faker.seed(args.seed)

# Define categorical data lists
genders = ['Male', 'Female', 'Other']
occupations = ['Engineer', 'Teacher', 'Doctor', 'Artist', 'Manager', 'Student', 'Retired', 'Unemployed']
education_levels = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD']
payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet', 'Bank Transfer']
spending_categories = ['Food', 'Entertainment', 'Travel', 'Utilities', 'Healthcare', 'Education', 'Transportation', 'Shopping']
corporate_spending_categories = ['Raw Materials', 'Salaries', 'Marketing', 'R&D', 'Utilities', 'Rent', 'Equipment']
platforms = ['Facebook', 'Twitter', 'Instagram', 'LinkedIn', 'TikTok']
topics = ['Technology', 'Fashion', 'Sports', 'Politics', 'Entertainment', 'Finance', 'Health', 'Travel']
brands = ['Apple', 'Nike', 'Coca-Cola', 'Tesla', 'Amazon', 'Google', 'Microsoft', 'Samsung']
influencers = ['InfluencerA', 'InfluencerB', 'InfluencerC', 'InfluencerD', 'InfluencerE']
sentiments = ['Positive', 'Neutral', 'Negative']
concerns = ['Billing Issue', 'Account Access', 'Product Inquiry', 'Technical Support', 'Complaint', 'Feedback']
purchase_platforms = ['Online', 'In-store', 'Mobile App']
item_categories = ['Electronics', 'Clothing', 'Groceries', 'Home Goods', 'Books', 'Toys']
item_subcategories = {
    'Electronics': ['Phones', 'Laptops', 'Tablets', 'Cameras'],
    'Clothing': ['Men', 'Women', 'Kids', 'Accessories'],
    'Groceries': ['Produce', 'Dairy', 'Meat', 'Bakery'],
    'Home Goods': ['Furniture', 'Decor', 'Kitchen', 'Bedding'],
    'Books': ['Fiction', 'Non-Fiction', 'Children', 'Textbooks'],
    'Toys': ['Action Figures', 'Dolls', 'Puzzles', 'Outdoor']
}
purchase_brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']

# Generate Customer Profiles
customer_profiles = []
for i in range(1, args.customer_count + 1):
    num_loans = random.randint(0, 5)
    customer = {
        'Customer ID': i,
        'Age': random.randint(18, 80),
        'Gender': random.choice(genders),
        'Income': round(random.uniform(20000, 200000), 2),
        'Occupation': random.choice(occupations),
        'Credit Score': random.randint(300, 850),
        'Preffered Payment Method': random.choice(payment_methods),
        'Recent Large Purchases': random.randint(0, 5),
        'Location': fake.city(),
        'Education': random.choice(education_levels),
        'Avg past 3 month end bank balance': round(random.uniform(100, 100000), 2),
        'Is married': random.choice([True, False]),
        'Num children': random.randint(0, 5),
        'Num loans': num_loans,
        'Loans Amt Dollar': round(sum([random.uniform(1000, 50000) for _ in range(num_loans)]), 2),
        'Avg monthy spending': round(random.uniform(500, 10000), 2),
        'Top spending categories': ', '.join(random.sample(spending_categories, 3)),
        'Num of support interactions last 3 month': random.randint(0, 10)
    }
    customer_profiles.append(customer)
customer_df = pd.DataFrame(customer_profiles)
customer_df.to_csv('Customer_Profile.csv', index=False)

# Generate Corporate Profiles
corporate_profiles = []
for i in range(args.customer_count + 1, args.customer_count + args.corporate_count + 1):
    corporate = {
        'Customer ID': i,
        'Num employees': random.randint(1, 10000),
        'Yearly Revenue': round(random.uniform(10000, 1000000000), 2),
        'Location': fake.city(),
        'Years in business': random.randint(1, 100),
        'Profit margins': round(random.uniform(0.01, 0.5), 2),
        'Past year growth percent': round(random.uniform(-20, 50), 2),
        'Avg past 3 month end acc balance': round(random.uniform(1000, 10000000), 2),
        'Top spending categories': ', '.join(random.sample(corporate_spending_categories, 3)),
        'Loan amt': round(random.uniform(0, 100000000), 2),
        'Num of support interactions last 3 month': random.randint(0, 20)
    }
    corporate_profiles.append(corporate)
corporate_df = pd.DataFrame(corporate_profiles)
corporate_df.to_csv('Corporate_Profile.csv', index=False)

# Generate Social Media Records
all_customer_ids = list(range(1, args.customer_count + args.corporate_count + 1))
social_media_records = []
for customer_id in all_customer_ids:
    num_records = random.randint(0, 10)
    for _ in range(num_records):
        record = {
            'Customer ID': customer_id,
            'Date': fake.date_between(start_date='-1y', end_date='today'),
            'Platform': random.choice(platforms),
            'Image Url': f'http://example.com/image{random.randint(1,1000)}.jpg',
            'Text Content': fake.sentence(nb_words=10),
            'Sentiment Score': round(random.uniform(-1, 1), 2),
            'Engagement Level': random.choice(['Low', 'Medium', 'High']),
            'Topics of Interest': ', '.join(random.sample(topics, random.randint(1, 3))),
            'Brands Liked': ', '.join(random.sample(brands, random.randint(0, 5))),
            'Influencers Followed': ', '.join(random.sample(influencers, random.randint(0, 5))),
            'Feedback on Financial Products': fake.sentence(nb_words=5)
        }
        social_media_records.append(record)
social_media_df = pd.DataFrame(social_media_records)
social_media_df.to_csv('Social_Media_Record.csv', index=False)

# Generate Customer Support Records
support_records = []
for customer_id in all_customer_ids:
    num_records = random.randint(0, 5)
    for _ in range(num_records):
        record = {
            'Customer ID': customer_id,
            'Date': fake.date_between(start_date='-1y', end_date='today'),
            'Audio Url': f'http://example.com/audio{random.randint(1,1000)}.mp3',
            'Transcript': fake.paragraph(nb_sentences=3),
            'Sentiment': random.choice(sentiments),
            'Was issue resolved': random.choice([True, False]),
            'Is repeating issue': random.choice([True, False]),
            'Main concerns': ', '.join(random.sample(concerns, random.randint(1, 2)))
        }
        support_records.append(record)
support_df = pd.DataFrame(support_records)
support_df.to_csv('Customer_Support_Record.csv', index=False)

# Generate Customer Purchase Records
purchase_records = []
for customer_id in all_customer_ids:
    num_records = random.randint(0, 20)
    for _ in range(num_records):
        category = random.choice(item_categories)
        subcategory = random.choice(item_subcategories[category])
        record = {
            'Customer ID': customer_id,
            'Date': fake.date_between(start_date='-1y', end_date='today'),
            'Platform': random.choice(purchase_platforms),
            'Payment Method': random.choice(payment_methods),
            'Amt': round(random.uniform(1, 10000), 2),
            'Location': fake.city(),
            'Item Category': category,
            'Item Sub Category': subcategory,
            'Item brand': random.choice(purchase_brands)
        }
        purchase_records.append(record)
purchase_df = pd.DataFrame(purchase_records)
purchase_df.to_csv('Customer_Purchase_Record.csv', index=False)