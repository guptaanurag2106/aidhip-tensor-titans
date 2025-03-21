import json
import random

def generate_financial_products():
    
    product_categories = {
        "Credit Card": [
            "Basic", "Gold", "Platinum", "Business", "Student", 
            "Travel", "Dining", "Amazon", "Fuel", "Luxury"
        ],
        "Insurance": [
            "Home", "Health", "Life", "Auto", "Travel", "Pet", "Business"
        ],
        "Loan": [
            "Personal", "Home", "Vehicle", "Education", "Business"
        ],
        "Investment": [
            "Mutual Fund", "FD", "Stocks", "Gold", "Real Estate"
        ]
    }
    
    
    tiers = ["Entry", "Standard", "Premium", "Elite"]
    
    
    base_attributes = {
        # Credit Cards
        "Basic": {"risk_customer": 2, "value_customer": 3, "profit_margin": 4, "risk_bank": 2, "retention_value": 2},
        "Gold": {"risk_customer": 3, "value_customer": 5, "profit_margin": 5, "risk_bank": 3, "retention_value": 4},
        "Platinum": {"risk_customer": 4, "value_customer": 7, "profit_margin": 7, "risk_bank": 4, "retention_value": 6},
        "Business": {"risk_customer": 5, "value_customer": 6, "profit_margin": 6, "risk_bank": 5, "retention_value": 7},
        "Student": {"risk_customer": 4, "value_customer": 3, "profit_margin": 3, "risk_bank": 6, "retention_value": 5},
        "Travel": {"risk_customer": 3, "value_customer": 6, "profit_margin": 5, "risk_bank": 3, "retention_value": 5},
        "Dining": {"risk_customer": 2, "value_customer": 5, "profit_margin": 4, "risk_bank": 2, "retention_value": 4},
        "Amazon": {"risk_customer": 2, "value_customer": 5, "profit_margin": 5, "risk_bank": 2, "retention_value": 5},
        "Fuel": {"risk_customer": 2, "value_customer": 5, "profit_margin": 4, "risk_bank": 2, "retention_value": 3},
        "Luxury": {"risk_customer": 5, "value_customer": 8, "profit_margin": 9, "risk_bank": 4, "retention_value": 7},
        
        # Insurance
        "Home": {"risk_customer": 3, "value_customer": 7, "profit_margin": 5, "risk_bank": 4, "retention_value": 6},
        "Health": {"risk_customer": 2, "value_customer": 8, "profit_margin": 6, "risk_bank": 7, "retention_value": 8},
        "Life": {"risk_customer": 2, "value_customer": 6, "profit_margin": 7, "risk_bank": 5, "retention_value": 7},
        "Auto": {"risk_customer": 3, "value_customer": 6, "profit_margin": 6, "risk_bank": 5, "retention_value": 5},
        "Travel": {"risk_customer": 4, "value_customer": 5, "profit_margin": 7, "risk_bank": 3, "retention_value": 3},
        "Pet": {"risk_customer": 3, "value_customer": 5, "profit_margin": 6, "risk_bank": 3, "retention_value": 4},
        "Business": {"risk_customer": 6, "value_customer": 7, "profit_margin": 8, "risk_bank": 6, "retention_value": 7},
        
        # Loans
        "Personal": {"risk_customer": 5, "value_customer": 6, "profit_margin": 7, "risk_bank": 7, "retention_value": 4},
        "Home": {"risk_customer": 7, "value_customer": 8, "profit_margin": 6, "risk_bank": 5, "retention_value": 8},
        "Vehicle": {"risk_customer": 5, "value_customer": 6, "profit_margin": 5, "risk_bank": 4, "retention_value": 5},
        "Education": {"risk_customer": 6, "value_customer": 7, "profit_margin": 4, "risk_bank": 5, "retention_value": 6},
        "Business": {"risk_customer": 8, "value_customer": 7, "profit_margin": 8, "risk_bank": 9, "retention_value": 6},
        
        # Investments
        "Mutual Fund": {"risk_customer": 5, "value_customer": 6, "profit_margin": 5, "risk_bank": 3, "retention_value": 6},
        "FD": {"risk_customer": 1, "value_customer": 4, "profit_margin": 3, "risk_bank": 1, "retention_value": 5},
        "Stocks": {"risk_customer": 8, "value_customer": 7, "profit_margin": 6, "risk_bank": 4, "retention_value": 6},
        "Gold": {"risk_customer": 3, "value_customer": 5, "profit_margin": 4, "risk_bank": 2, "retention_value": 5},
        "Real Estate": {"risk_customer": 7, "value_customer": 7, "profit_margin": 5, "risk_bank": 4, "retention_value": 7},
    }
    
   
    product_details = {
        "Credit Card": {
            "interest_rate": {
                "Basic": {"Entry": 21.99, "Standard": 19.99, "Premium": 18.99, "Elite": 17.99},
                "Gold": {"Entry": 19.99, "Standard": 18.99, "Premium": 17.99, "Elite": 16.99},
                "Platinum": {"Entry": 18.99, "Standard": 17.99, "Premium": 16.99, "Elite": 15.99},
                "Business": {"Entry": 18.99, "Standard": 17.99, "Premium": 16.99, "Elite": 15.99},
                "Student": {"Entry": 19.99, "Standard": 18.99, "Premium": 17.99, "Elite": 16.99},
                "Travel": {"Entry": 20.99, "Standard": 19.99, "Premium": 18.99, "Elite": 17.99},
                "Dining": {"Entry": 20.99, "Standard": 19.99, "Premium": 18.99, "Elite": 17.99},
                "Amazon": {"Entry": 20.99, "Standard": 19.99, "Premium": 18.99, "Elite": 17.99},
                "Fuel": {"Entry": 21.99, "Standard": 20.99, "Premium": 19.99, "Elite": 18.99},
                "Luxury": {"Entry": 17.99, "Standard": 16.99, "Premium": 15.99, "Elite": 14.99}
            },
            "annual_fee": {
                "Basic": {"Entry": 0, "Standard": 25, "Premium": 50, "Elite": 75},
                "Gold": {"Entry": 50, "Standard": 95, "Premium": 150, "Elite": 195},
                "Platinum": {"Entry": 95, "Standard": 195, "Premium": 295, "Elite": 395},
                "Business": {"Entry": 75, "Standard": 125, "Premium": 195, "Elite": 295},
                "Student": {"Entry": 0, "Standard": 0, "Premium": 25, "Elite": 45},
                "Travel": {"Entry": 75, "Standard": 150, "Premium": 250, "Elite": 350},
                "Dining": {"Entry": 50, "Standard": 95, "Premium": 150, "Elite": 195},
                "Amazon": {"Entry": 0, "Standard": 49, "Premium": 99, "Elite": 149},
                "Fuel": {"Entry": 25, "Standard": 50, "Premium": 95, "Elite": 145},
                "Luxury": {"Entry": 195, "Standard": 295, "Premium": 495, "Elite": 695}
            },
            "credit_limit": {
                "Basic": {"Entry": 1000, "Standard": 2500, "Premium": 5000, "Elite": 7500},
                "Gold": {"Entry": 5000, "Standard": 10000, "Premium": 15000, "Elite": 20000},
                "Platinum": {"Entry": 10000, "Standard": 20000, "Premium": 30000, "Elite": 50000},
                "Business": {"Entry": 5000, "Standard": 15000, "Premium": 25000, "Elite": 50000},
                "Student": {"Entry": 500, "Standard": 1000, "Premium": 1500, "Elite": 2500},
                "Travel": {"Entry": 3000, "Standard": 7500, "Premium": 15000, "Elite": 25000},
                "Dining": {"Entry": 2000, "Standard": 5000, "Premium": 10000, "Elite": 15000},
                "Amazon": {"Entry": 1500, "Standard": 3000, "Premium": 6000, "Elite": 10000},
                "Fuel": {"Entry": 1500, "Standard": 3000, "Premium": 5000, "Elite": 7500},
                "Luxury": {"Entry": 10000, "Standard": 25000, "Premium": 50000, "Elite": 100000}
            },
            "rewards_rate": {
                "Basic": {"Entry": 1.0, "Standard": 1.5, "Premium": 2.0, "Elite": 2.5},
                "Gold": {"Entry": 1.5, "Standard": 2.0, "Premium": 2.5, "Elite": 3.0},
                "Platinum": {"Entry": 2.0, "Standard": 2.5, "Premium": 3.0, "Elite": 4.0},
                "Business": {"Entry": 1.5, "Standard": 2.0, "Premium": 2.5, "Elite": 3.0},
                "Student": {"Entry": 1.0, "Standard": 1.25, "Premium": 1.5, "Elite": 2.0},
                "Travel": {"Entry": 2.0, "Standard": 3.0, "Premium": 4.0, "Elite": 5.0},
                "Dining": {"Entry": 3.0, "Standard": 4.0, "Premium": 5.0, "Elite": 6.0},
                "Amazon": {"Entry": 3.0, "Standard": 4.0, "Premium": 5.0, "Elite": 6.0},
                "Fuel": {"Entry": 3.0, "Standard": 4.0, "Premium": 5.0, "Elite": 6.0},
                "Luxury": {"Entry": 2.5, "Standard": 3.5, "Premium": 4.5, "Elite": 5.5}
            }
        },
        "Insurance": {
            "monthly_premium": {
                "Home": {"Entry": 25, "Standard": 50, "Premium": 100, "Elite": 150},
                "Health": {"Entry": 100, "Standard": 250, "Premium": 400, "Elite": 600},
                "Life": {"Entry": 20, "Standard": 45, "Premium": 95, "Elite": 150},
                "Auto": {"Entry": 50, "Standard": 100, "Premium": 150, "Elite": 200},
                "Travel": {"Entry": 15, "Standard": 25, "Premium": 45, "Elite": 75},
                "Pet": {"Entry": 20, "Standard": 35, "Premium": 50, "Elite": 75},
                "Business": {"Entry": 100, "Standard": 250, "Premium": 500, "Elite": 1000}
            },
            "deductible": {
                "Home": {"Entry": 1000, "Standard": 750, "Premium": 500, "Elite": 250},
                "Health": {"Entry": 2000, "Standard": 1500, "Premium": 1000, "Elite": 500},
                "Life": {"Entry": 0, "Standard": 0, "Premium": 0, "Elite": 0},
                "Auto": {"Entry": 1000, "Standard": 750, "Premium": 500, "Elite": 250},
                "Travel": {"Entry": 250, "Standard": 150, "Premium": 100, "Elite": 50},
                "Pet": {"Entry": 500, "Standard": 350, "Premium": 250, "Elite": 100},
                "Business": {"Entry": 2000, "Standard": 1500, "Premium": 1000, "Elite": 500}
            },
            "coverage_amount": {
                "Home": {"Entry": 100000, "Standard": 250000, "Premium": 500000, "Elite": 1000000},
                "Health": {"Entry": 500000, "Standard": 1000000, "Premium": 3000000, "Elite": 5000000},
                "Life": {"Entry": 100000, "Standard": 250000, "Premium": 500000, "Elite": 1000000},
                "Auto": {"Entry": 50000, "Standard": 100000, "Premium": 250000, "Elite": 500000},
                "Travel": {"Entry": 25000, "Standard": 50000, "Premium": 100000, "Elite": 250000},
                "Pet": {"Entry": 5000, "Standard": 10000, "Premium": 15000, "Elite": 25000},
                "Business": {"Entry": 250000, "Standard": 500000, "Premium": 1000000, "Elite": 5000000}
            }
        },
        "Loan": {
            "interest_rate": {
                "Personal": {"Entry": 12.99, "Standard": 10.99, "Premium": 9.49, "Elite": 7.99},
                "Home": {"Entry": 6.99, "Standard": 5.99, "Premium": 4.99, "Elite": 3.99},
                "Vehicle": {"Entry": 7.99, "Standard": 6.99, "Premium": 5.99, "Elite": 4.99},
                "Education": {"Entry": 6.49, "Standard": 5.49, "Premium": 4.49, "Elite": 3.49},
                "Business": {"Entry": 9.99, "Standard": 8.99, "Premium": 7.99, "Elite": 6.99}
            },
            "loan_amount": {
                "Personal": {"Entry": 5000, "Standard": 15000, "Premium": 30000, "Elite": 50000},
                "Home": {"Entry": 100000, "Standard": 300000, "Premium": 600000, "Elite": 1000000},
                "Vehicle": {"Entry": 10000, "Standard": 25000, "Premium": 50000, "Elite": 100000},
                "Education": {"Entry": 10000, "Standard": 25000, "Premium": 50000, "Elite": 100000},
                "Business": {"Entry": 25000, "Standard": 100000, "Premium": 250000, "Elite": 500000}
            },
            "term_months": {
                "Personal": {"Entry": 24, "Standard": 36, "Premium": 48, "Elite": 60},
                "Home": {"Entry": 180, "Standard": 240, "Premium": 300, "Elite": 360},
                "Vehicle": {"Entry": 36, "Standard": 48, "Premium": 60, "Elite": 72},
                "Education": {"Entry": 60, "Standard": 120, "Premium": 180, "Elite": 240},
                "Business": {"Entry": 36, "Standard": 60, "Premium": 84, "Elite": 120}
            }
        },
        "Investment": {
            "min_investment": {
                "Mutual Fund": {"Entry": 1000, "Standard": 5000, "Premium": 10000, "Elite": 25000},
                "FD": {"Entry": 500, "Standard": 2500, "Premium": 10000, "Elite": 25000},
                "Stocks": {"Entry": 100, "Standard": 1000, "Premium": 5000, "Elite": 20000},
                "Gold": {"Entry": 500, "Standard": 2500, "Premium": 10000, "Elite": 25000},
                "Real Estate": {"Entry": 10000, "Standard": 50000, "Premium": 100000, "Elite": 250000}                
            },
            "expected_annual_return": {
                "Mutual Fund": {"Entry": 6.0, "Standard": 8.0, "Premium": 10.0, "Elite": 12.0},
                "FD": {"Entry": 2.0, "Standard": 2.5, "Premium": 3.0, "Elite": 3.5},
                "Stocks": {"Entry": 7.0, "Standard": 10.0, "Premium": 12.0, "Elite": 15.0},
                "Gold": {"Entry": 3.0, "Standard": 4.0, "Premium": 5.0, "Elite": 6.0},
                "Real Estate": {"Entry": 5.0, "Standard": 7.0, "Premium": 9.0, "Elite": 12.0}                
            },
            "volatility": {
                "Mutual Fund": {"Entry": 3, "Standard": 4, "Premium": 5, "Elite": 6},
                "FD": {"Entry": 1, "Standard": 1, "Premium": 1, "Elite": 1},
                "Stocks": {"Entry": 6, "Standard": 7, "Premium": 8, "Elite": 9},
                "Gold": {"Entry": 3, "Standard": 3, "Premium": 4, "Elite": 4},
                "Real Estate": {"Entry": 2, "Standard": 3, "Premium": 4, "Elite": 5}                
            }
        }
    }
    
    
    tier_modifiers = {
        "Entry": {"risk_customer": 0.8, "value_customer": 0.7, "profit_margin": 0.8, "risk_bank": 1.2, "retention_value": 0.7},
        "Standard": {"risk_customer": 1.0, "value_customer": 1.0, "profit_margin": 1.0, "risk_bank": 1.0, "retention_value": 1.0},
        "Premium": {"risk_customer": 1.2, "value_customer": 1.3, "profit_margin": 1.2, "risk_bank": 0.9, "retention_value": 1.3},
        "Elite": {"risk_customer": 1.4, "value_customer": 1.6, "profit_margin": 1.4, "risk_bank": 0.8, "retention_value": 1.6}
    }
    
    
    products = []
    product_id = 1
    
    for category, subcategories in product_categories.items():
        for subcategory in subcategories:
            for tier in tiers:
                
                base_attrs = base_attributes[subcategory]
                
               
                modified_attrs = {
                    attr: min(10, max(1, round(base_attrs[attr] * tier_modifiers[tier][attr])))
                    for attr in base_attrs
                }
                
                
                details = {}
                for detail_type, detail_values in product_details[category].items():
                    if subcategory in detail_values and tier in detail_values[subcategory]:
                        details[detail_type] = detail_values[subcategory][tier]
                
                
                product = {
                    "product_id": f"PROD_{product_id}",
                    "category": category,
                    "subcategory": subcategory,
                    "tier": tier,
                    "name": f"{tier} {subcategory} {category}",
                    "description": f"{tier.lower()} level {subcategory.lower()} {category.lower()} product.",
                    "risk_customer": modified_attrs["risk_customer"],
                    "value_customer": modified_attrs["value_customer"],
                    "profit_margin": modified_attrs["profit_margin"],
                    "risk_bank": modified_attrs["risk_bank"],
                    "retention_value": modified_attrs["retention_value"],
                    "details": details
                }
                
                products.append(product)
                product_id += 1
    
    return products

def main():
    products = generate_financial_products()
    
    
    with open('financial_products.json', 'w') as f:
        json.dump(products, f, indent=2)
    

if __name__ == "__main__":
    main()
