import json
import random

def generate_org_financial_products():
    
    product_categories = {
        "Credit Card": [
            "Basic", "Gold", "Platinum", "Luxury", "Dining", "Travel"
        ],
        "Insurance": [
            "Commercial Property", "Cybersecurity", "General Liability"
        ],
        "Loan": [
            "Working Capital", "Commercial Real Estate", "Trade Credit", "Startup Funding"
        ],
        "Investment": [
            "Corporate FD", "Government & Corporate Bonds", "REITs", "ETFs"
        ]
    }
    
    tiers = ["Entry", "Standard", "Premium", "Elite"]
    
    base_attributes = {
        # Credit Cards
        "Basic": {"risk_customer": 3, "value_customer": 4, "profit_margin": 5, "risk_bank": 3, "retention_value": 3},
        "Gold": {"risk_customer": 4, "value_customer": 6, "profit_margin": 6, "risk_bank": 4, "retention_value": 5},
        "Platinum": {"risk_customer": 5, "value_customer": 8, "profit_margin": 8, "risk_bank": 5, "retention_value": 7},
        "Luxury": {"risk_customer": 6, "value_customer": 9, "profit_margin": 9, "risk_bank": 5, "retention_value": 8},
        "Dining": {"risk_customer": 3, "value_customer": 7, "profit_margin": 6, "risk_bank": 3, "retention_value": 6},
        "Travel": {"risk_customer": 4, "value_customer": 8, "profit_margin": 7, "risk_bank": 4, "retention_value": 7},
        
        # Insurance
        "Commercial Property": {"risk_customer": 6, "value_customer": 8, "profit_margin": 7, "risk_bank": 7, "retention_value": 7},
        "Cybersecurity": {"risk_customer": 5, "value_customer": 9, "profit_margin": 8, "risk_bank": 8, "retention_value": 8},
        "General Liability": {"risk_customer": 5, "value_customer": 8, "profit_margin": 7, "risk_bank": 6, "retention_value": 7},
        
        # Loans
        "Working Capital": {"risk_customer": 6, "value_customer": 7, "profit_margin": 6, "risk_bank": 6, "retention_value": 5},
        "Commercial Real Estate": {"risk_customer": 8, "value_customer": 7, "profit_margin": 7, "risk_bank": 7, "retention_value": 8},
        "Trade Credit": {"risk_customer": 7, "value_customer": 8, "profit_margin": 7, "risk_bank": 8, "retention_value": 6},
        "Startup Funding": {"risk_customer": 9, "value_customer": 8, "profit_margin": 8, "risk_bank": 9, "retention_value": 7},
        
        # Investments
        "Corporate FD": {"risk_customer": 2, "value_customer": 5, "profit_margin": 4, "risk_bank": 2, "retention_value": 6},
        "Government & Corporate Bonds": {"risk_customer": 3, "value_customer": 6, "profit_margin": 4, "risk_bank": 3, "retention_value": 6},
        "REITs": {"risk_customer": 6, "value_customer": 7, "profit_margin": 6, "risk_bank": 5, "retention_value": 7},
        "ETFs": {"risk_customer": 5, "value_customer": 6, "profit_margin": 5, "risk_bank": 4, "retention_value": 6}
    }
    
    
    product_details = {
        "Credit Card": {
            "interest_rate": {
                "Basic": {"Entry": 18.99, "Standard": 17.99, "Premium": 16.99, "Elite": 15.99},
                "Gold": {"Entry": 17.99, "Standard": 16.99, "Premium": 15.99, "Elite": 14.99},
                "Platinum": {"Entry": 16.99, "Standard": 15.99, "Premium": 14.99, "Elite": 13.99},
                "Luxury": {"Entry": 16.49, "Standard": 15.49, "Premium": 14.49, "Elite": 13.49},
                "Dining": {"Entry": 17.99, "Standard": 16.99, "Premium": 15.99, "Elite": 14.99},
                "Travel": {"Entry": 17.99, "Standard": 16.99, "Premium": 15.99, "Elite": 14.99}
            },
            "annual_fee": {
                "Basic": {"Entry": 0, "Standard": 50, "Premium": 100, "Elite": 150},
                "Gold": {"Entry": 100, "Standard": 195, "Premium": 295, "Elite": 395},
                "Platinum": {"Entry": 195, "Standard": 295, "Premium": 495, "Elite": 695},
                "Luxury": {"Entry": 295, "Standard": 495, "Premium": 795, "Elite": 995},
                "Dining": {"Entry": 150, "Standard": 250, "Premium": 350, "Elite": 495},
                "Travel": {"Entry": 175, "Standard": 275, "Premium": 375, "Elite": 550}
            },
            "credit_limit": {
                "Basic": {"Entry": 10000, "Standard": 20000, "Premium": 35000, "Elite": 50000},
                "Gold": {"Entry": 20000, "Standard": 40000, "Premium": 60000, "Elite": 100000},
                "Platinum": {"Entry": 50000, "Standard": 100000, "Premium": 150000, "Elite": 250000},
                "Luxury": {"Entry": 100000, "Standard": 200000, "Premium": 350000, "Elite": 500000},
                "Dining": {"Entry": 25000, "Standard": 50000, "Premium": 75000, "Elite": 100000},
                "Travel": {"Entry": 30000, "Standard": 60000, "Premium": 100000, "Elite": 150000}
            },
            "rewards_rate": {
                "Basic": {"Entry": 1.5, "Standard": 2.0, "Premium": 2.5, "Elite": 3.0},
                "Gold": {"Entry": 2.0, "Standard": 2.5, "Premium": 3.0, "Elite": 3.5},
                "Platinum": {"Entry": 2.5, "Standard": 3.0, "Premium": 3.5, "Elite": 4.5},
                "Luxury": {"Entry": 3.0, "Standard": 4.0, "Premium": 5.0, "Elite": 6.0},
                "Dining": {"Entry": 4.0, "Standard": 5.0, "Premium": 6.0, "Elite": 7.0},
                "Travel": {"Entry": 4.0, "Standard": 5.0, "Premium": 6.0, "Elite": 7.0}
            },
            "employee_cards": {
                "Basic": {"Entry": 3, "Standard": 5, "Premium": 10, "Elite": 15},
                "Gold": {"Entry": 5, "Standard": 10, "Premium": 15, "Elite": 25},
                "Platinum": {"Entry": 10, "Standard": 20, "Premium": 30, "Elite": 50},
                "Luxury": {"Entry": 15, "Standard": 25, "Premium": 50, "Elite": 100},
                "Dining": {"Entry": 5, "Standard": 10, "Premium": 20, "Elite": 30},
                "Travel": {"Entry": 5, "Standard": 15, "Premium": 25, "Elite": 40}
            }
        },
        "Insurance": {
            "monthly_premium": {
                "Commercial Property": {"Entry": 500, "Standard": 1000, "Premium": 2000, "Elite": 3500},
                "Cybersecurity": {"Entry": 350, "Standard": 750, "Premium": 1500, "Elite": 3000},
                "General Liability": {"Entry": 300, "Standard": 600, "Premium": 1200, "Elite": 2000}
            },
            "deductible": {
                "Commercial Property": {"Entry": 10000, "Standard": 7500, "Premium": 5000, "Elite": 2500},
                "Cybersecurity": {"Entry": 15000, "Standard": 10000, "Premium": 7500, "Elite": 5000},
                "General Liability": {"Entry": 5000, "Standard": 3500, "Premium": 2500, "Elite": 1000}
            },
            "coverage_amount": {
                "Commercial Property": {"Entry": 500000, "Standard": 1000000, "Premium": 2500000, "Elite": 5000000},
                "Cybersecurity": {"Entry": 1000000, "Standard": 2500000, "Premium": 5000000, "Elite": 10000000},
                "General Liability": {"Entry": 1000000, "Standard": 2000000, "Premium": 5000000, "Elite": 10000000}
            },
            "specialized_coverage": {
                "Commercial Property": {"Entry": "Basic", "Standard": "Standard", "Premium": "Comprehensive", "Elite": "All-inclusive"},
                "Cybersecurity": {"Entry": "Data Breach", "Standard": "Breach & Recovery", "Premium": "Full Cyber Protection", "Elite": "Enterprise Cyber Shield"},
                "General Liability": {"Entry": "Basic Liability", "Standard": "Standard Liability", "Premium": "Extended Liability", "Elite": "Complete Liability Shield"}
            }
        },
        "Loan": {
            "interest_rate": {
                "Working Capital": {"Entry": 8.99, "Standard": 7.99, "Premium": 6.99, "Elite": 5.99},
                "Commercial Real Estate": {"Entry": 6.49, "Standard": 5.99, "Premium": 5.49, "Elite": 4.99},
                "Trade Credit": {"Entry": 7.99, "Standard": 6.99, "Premium": 5.99, "Elite": 4.99},
                "Startup Funding": {"Entry": 9.99, "Standard": 8.99, "Premium": 7.99, "Elite": 6.99}
            },
            "loan_amount": {
                "Working Capital": {"Entry": 50000, "Standard": 150000, "Premium": 500000, "Elite": 1000000},
                "Commercial Real Estate": {"Entry": 250000, "Standard": 750000, "Premium": 2000000, "Elite": 5000000},
                "Trade Credit": {"Entry": 100000, "Standard": 250000, "Premium": 500000, "Elite": 1000000},
                "Startup Funding": {"Entry": 50000, "Standard": 200000, "Premium": 500000, "Elite": 1000000}
            },
            "term_months": {
                "Working Capital": {"Entry": 12, "Standard": 24, "Premium": 36, "Elite": 48},
                "Commercial Real Estate": {"Entry": 120, "Standard": 180, "Premium": 240, "Elite": 360},
                "Trade Credit": {"Entry": 6, "Standard": 12, "Premium": 24, "Elite": 36},
                "Startup Funding": {"Entry": 36, "Standard": 48, "Premium": 60, "Elite": 84}
            },
            "processing_fee": {
                "Working Capital": {"Entry": 2.0, "Standard": 1.5, "Premium": 1.0, "Elite": 0.5},
                "Commercial Real Estate": {"Entry": 1.5, "Standard": 1.0, "Premium": 0.75, "Elite": 0.5},
                "Trade Credit": {"Entry": 2.0, "Standard": 1.5, "Premium": 1.0, "Elite": 0.5},
                "Startup Funding": {"Entry": 3.0, "Standard": 2.0, "Premium": 1.0, "Elite": 0.5}
            }
        },
        "Investment": {
            "min_investment": {
                "Corporate FD": {"Entry": 10000, "Standard": 50000, "Premium": 100000, "Elite": 500000},
                "Government & Corporate Bonds": {"Entry": 25000, "Standard": 100000, "Premium": 250000, "Elite": 1000000},
                "REITs": {"Entry": 50000, "Standard": 150000, "Premium": 500000, "Elite": 1000000},
                "ETFs": {"Entry": 10000, "Standard": 50000, "Premium": 100000, "Elite": 250000}
            },
            "expected_annual_return": {
                "Corporate FD": {"Entry": 3.0, "Standard": 3.5, "Premium": 4.0, "Elite": 4.5},
                "Government & Corporate Bonds": {"Entry": 4.0, "Standard": 5.0, "Premium": 6.0, "Elite": 7.0},
                "REITs": {"Entry": 6.0, "Standard": 8.0, "Premium": 10.0, "Elite": 12.0},
                "ETFs": {"Entry": 5.0, "Standard": 7.0, "Premium": 9.0, "Elite": 11.0}
            },
            "volatility": {
                "Corporate FD": {"Entry": 1, "Standard": 1, "Premium": 1, "Elite": 1},
                "Government & Corporate Bonds": {"Entry": 2, "Standard": 2, "Premium": 3, "Elite": 3},
                "REITs": {"Entry": 4, "Standard": 5, "Premium": 6, "Elite": 7},
                "ETFs": {"Entry": 3, "Standard": 4, "Premium": 5, "Elite": 6}
            },
            "lock_in_period_months": {
                "Corporate FD": {"Entry": 6, "Standard": 12, "Premium": 24, "Elite": 36},
                "Government & Corporate Bonds": {"Entry": 12, "Standard": 24, "Premium": 36, "Elite": 60},
                "REITs": {"Entry": 6, "Standard": 12, "Premium": 24, "Elite": 36},
                "ETFs": {"Entry": 0, "Standard": 0, "Premium": 0, "Elite": 0}
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
       
                description, benefits = generate_description_and_benefits(category, subcategory, tier)
                
                
                product = {
                    "product_id": f"ORG_PROD_{product_id}",
                    "category": category,
                    "subcategory": subcategory,
                    "tier": tier,
                    "name": f"{tier} {subcategory} {category} for Organizations",
                    "description": description,
                    "benefits": benefits,
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

def generate_description_and_benefits(category, subcategory, tier):
    """Generate detailed descriptions and benefits for each product"""
    
    descriptions = {
        "Credit Card": {
            "Basic": {
                "Entry": "Essential business credit card with basic rewards and low annual fee.",
                "Standard": "Standard business credit card with moderate rewards and competitive rates.",
                "Premium": "Premium business credit card with enhanced rewards and benefits.",
                "Elite": "Elite business credit card with exceptional rewards and exclusive privileges."
            },
            "Gold": {
                "Entry": "Entry-level Gold business card with enhanced cashback on business expenses.",
                "Standard": "Standard Gold business card with superior rewards and travel benefits.",
                "Premium": "Premium Gold business card with extensive rewards and premium services.",
                "Elite": "Elite Gold business card with maximum rewards and exclusive concierge services."
            },
            "Platinum": {
                "Entry": "Entry-level Platinum business card with premium rewards and benefits.",
                "Standard": "Standard Platinum business card with extensive travel and business perks.",
                "Premium": "Premium Platinum business card with comprehensive rewards and executive benefits.",
                "Elite": "Elite Platinum business card with unlimited rewards and exclusive global privileges."
            },
            "Luxury": {
                "Entry": "Entry-level Luxury business card with premium status and exclusive rewards.",
                "Standard": "Standard Luxury business card with extensive privileges and premium services.",
                "Premium": "Premium Luxury business card with comprehensive concierge and global benefits.",
                "Elite": "Elite Luxury business card with unlimited privileges and tailored executive services."
            },
            "Dining": {
                "Entry": "Entry-level Dining business card with enhanced rewards on restaurant expenses.",
                "Standard": "Standard Dining business card with superior rewards on dining and catering.",
                "Premium": "Premium Dining business card with extensive rewards on all food-related expenses.",
                "Elite": "Elite Dining business card with maximum rewards on hospitality and exclusive restaurant access."
            },
            "Travel": {
                "Entry": "Entry-level Travel business card with enhanced rewards on travel expenses.",
                "Standard": "Standard Travel business card with superior travel benefits and insurance.",
                "Premium": "Premium Travel business card with extensive global travel rewards and lounge access.",
                "Elite": "Elite Travel business card with maximum travel rewards and comprehensive global benefits."
            }
        },
        "Insurance": {
            "Commercial Property": {
                "Entry": "Basic property insurance for small business premises and assets.",
                "Standard": "Standard property insurance with enhanced coverage for medium-sized businesses.",
                "Premium": "Premium property insurance with comprehensive coverage for larger businesses.",
                "Elite": "Elite property insurance with all-inclusive coverage for enterprise-level organizations."
            },
            "Cybersecurity": {
                "Entry": "Basic cyber insurance for small businesses handling sensitive data.",
                "Standard": "Standard cyber insurance with enhanced protection for growing businesses.",
                "Premium": "Premium cyber insurance with extensive coverage for medium to large organizations.",
                "Elite": "Elite cyber insurance with comprehensive protection for enterprise-level organizations."
            },
            "General Liability": {
                "Entry": "Basic liability coverage protecting against common business lawsuits.",
                "Standard": "Standard liability coverage with enhanced protection for growing businesses.",
                "Premium": "Premium liability coverage with extensive protection for medium to large organizations.",
                "Elite": "Elite liability coverage with comprehensive protection for enterprise-level organizations."
            }
        },
        "Loan": {
            "Working Capital": {
                "Entry": "Basic short-term cash flow management loan for small businesses.",
                "Standard": "Standard working capital loan with improved terms for established businesses.",
                "Premium": "Premium working capital solution with favorable terms for larger businesses.",
                "Elite": "Elite working capital solution with optimal terms for major enterprises."
            },
            "Commercial Real Estate": {
                "Entry": "Basic commercial real estate loan for small office expansions.",
                "Standard": "Standard commercial real estate loan with improved terms for medium properties.",
                "Premium": "Premium commercial real estate financing for larger property investments.",
                "Elite": "Elite commercial real estate financing with optimal terms for major property acquisitions."
            },
            "Trade Credit": {
                "Entry": "Basic trade credit loan for small import/export businesses.",
                "Standard": "Standard trade credit financing with improved terms for established traders.",
                "Premium": "Premium trade credit solution with favorable terms for larger trading operations.",
                "Elite": "Elite trade credit solution with optimal terms for major international trading operations."
            },
            "Startup Funding": {
                "Entry": "Basic startup funding for newly registered small businesses.",
                "Standard": "Standard startup financing with improved terms for promising ventures.",
                "Premium": "Premium startup capital with favorable terms for high-potential businesses.",
                "Elite": "Elite startup financing with optimal terms for high-growth ventures."
            }
        },
        "Investment": {
            "Corporate FD": {
                "Entry": "Basic corporate fixed deposit with flexible tenure options.",
                "Standard": "Standard corporate fixed deposit with enhanced interest rates.",
                "Premium": "Premium corporate fixed deposit with preferential rates and terms.",
                "Elite": "Elite corporate fixed deposit with maximum returns and flexibility."
            },
            "Government & Corporate Bonds": {
                "Entry": "Basic bond investment portfolio focused on stable returns.",
                "Standard": "Standard bond investment with enhanced diversification and returns.",
                "Premium": "Premium bond portfolio with strategic allocation for optimal returns.",
                "Elite": "Elite bond investment solution with maximum yield optimization."
            },
            "REITs": {
                "Entry": "Basic REIT investment for income-generating real estate exposure.",
                "Standard": "Standard REIT investment with enhanced property portfolio diversification.",
                "Premium": "Premium REIT solution with strategic commercial property allocation.",
                "Elite": "Elite REIT investment with premium property holdings and maximum income potential."
            },
            "ETFs": {
                "Entry": "Basic ETF investment portfolio with core market exposure.",
                "Standard": "Standard ETF investment with enhanced sector diversification.",
                "Premium": "Premium ETF portfolio with strategic allocation across multiple asset classes.",
                "Elite": "Elite ETF investment solution with maximum diversification and liquidity benefits."
            }
        }
    }
    
    benefits = {
        "Credit Card": {
            "Basic": {
                "Entry": ["Low annual fee", "Basic expense tracking", "Up to 3 employee cards"],
                "Standard": ["Moderate rewards rate", "Basic expense reporting", "Up to 5 employee cards"],
                "Premium": ["Enhanced rewards", "Detailed expense categorization", "Up to 10 employee cards"],
                "Elite": ["Premium rewards", "Advanced expense analytics", "Up to 15 employee cards"]
            },
            "Gold": {
                "Entry": ["Enhanced cashback on business categories", "Basic travel insurance", "Up to 5 employee cards"],
                "Standard": ["Superior rewards on business expenses", "Comprehensive travel insurance", "Up to 10 employee cards"],
                "Premium": ["Extensive rewards program", "Premium travel benefits", "Up to 15 employee cards"],
                "Elite": ["Maximum rewards on all purchases", "Elite travel protection", "Up to 25 employee cards"]
            },
            "Platinum": {
                "Entry": ["Premium rewards on key business categories", "Airport lounge access", "Up to 10 employee cards"],
                "Standard": ["Extensive travel perks", "Global assistance", "Up to 20 employee cards"],
                "Premium": ["Comprehensive reward system", "Premium concierge", "Up to 30 employee cards"],
                "Elite": ["Unlimited rewards potential", "Global elite status", "Up to 50 employee cards"]
            },
            "Luxury": {
                "Entry": ["Premium status", "Luxury travel benefits", "Up to 15 employee cards"],
                "Standard": ["Extensive privileges", "Global concierge", "Up to 25 employee cards"],
                "Premium": ["Comprehensive luxury services", "VIP event access", "Up to 50 employee cards"],
                "Elite": ["Unlimited privileges", "Bespoke services", "Up to 100 employee cards"]
            },
            "Dining": {
                "Entry": ["Enhanced rewards on dining", "Restaurant reservations", "Up to 5 employee cards"],
                "Standard": ["Superior dining rewards", "Priority restaurant bookings", "Up to 10 employee cards"],
                "Premium": ["Extensive food & beverage rewards", "VIP dining experiences", "Up to 20 employee cards"],
                "Elite": ["Maximum dining rewards", "Exclusive chef experiences", "Up to 30 employee cards"]
            },
            "Travel": {
                "Entry": ["Enhanced travel rewards", "Basic travel insurance", "Up to 5 employee cards"],
                "Standard": ["Superior travel benefits", "Comprehensive travel protection", "Up to 15 employee cards"],
                "Premium": ["Extensive global rewards", "Premium lounge access", "Up to 25 employee cards"],
                "Elite": ["Maximum travel privileges", "Global elite status", "Up to 40 employee cards"]
            }
        },
        "Insurance": {
            "Commercial Property": {
                "Entry": ["Basic property protection", "Fire & theft coverage", "24/7 claims assistance"],
                "Standard": ["Enhanced property coverage", "Natural disaster protection", "Business interruption support"],
                "Premium": ["Comprehensive asset protection", "Full business interruption coverage", "Priority claims processing"],
                "Elite": ["All-inclusive coverage", "Bespoke risk assessment", "Dedicated claims team"]
            },
            "Cybersecurity": {
                "Entry": ["Basic data breach coverage", "Incident response support", "Regulatory compliance assistance"],
                "Standard": ["Enhanced cyber protection", "Business recovery services", "Legal defense coverage"],
                "Premium": ["Extensive cyber shield", "Crisis management", "Reputation protection"],
                "Elite": ["Comprehensive cyber protection", "24/7 monitoring", "Full incident remediation"]
            },
            "General Liability": {
                "Entry": ["Basic legal protection", "Third-party injury coverage", "Property damage liability"],
                "Standard": ["Enhanced liability coverage", "Product liability protection", "Legal defense costs"],
                "Premium": ["Extensive liability shield", "Advertising injury coverage", "Global protection"],
                "Elite": ["Comprehensive liability protection", "Directors & officers coverage", "Unlimited legal defense"]
            }
        },
        "Loan": {
            "Working Capital": {
                "Entry": ["Quick approval process", "Flexible repayment options", "No collateral for established businesses"],
                "Standard": ["Competitive interest rates", "Higher credit limits", "Reduced processing fees"],
                "Premium": ["Preferential interest rates", "Extended credit periods", "Minimal documentation"],
                "Elite": ["Lowest interest rates", "Maximum credit limits", "Zero processing fees"]
            },
            "Commercial Real Estate": {
                "Entry": ["Standard LTV ratio", "Fixed rate options", "Renovation financing available"],
                "Standard": ["Enhanced LTV options", "Competitive rates", "Flexible term structures"],
                "Premium": ["Preferred LTV ratios", "Reduced interest rates", "Comprehensive property assessment"],
                "Elite": ["Maximum LTV ratio", "Lowest interest rates", "Tailored repayment schedules"]
            },
            "Trade Credit": {
                "Entry": ["Basic import/export financing", "Letter of credit support", "Trade risk protection"],
                "Standard": ["Enhanced trade financing", "Global transaction support", "Reduced documentary fees"],
                "Premium": ["Comprehensive trade solutions", "Preferential exchange rates", "Priority processing"],
                "Elite": ["Elite trade financing", "Global banking network access", "Zero international fees"]
            },
            "Startup Funding": {
                "Entry": ["Basic startup capital", "Simplified application", "Business planning support"],
                "Standard": ["Enhanced funding options", "Reduced collateral requirements", "Mentorship access"],
                "Premium": ["Comprehensive startup package", "Minimal collateral needs", "Business development support"],
                "Elite": ["Maximum funding potential", "Collateral-free options", "Full business incubation support"]
            }
        },
        "Investment": {
            "Corporate FD": {
                "Entry": ["Higher than retail interest rates", "Flexible tenure options", "Premature withdrawal facility"],
                "Standard": ["Enhanced interest benefits", "Multiple reinvestment options", "Preferential rates"],
                "Premium": ["Premium interest rates", "Customized tenure options", "Sweep-in facility"],
                "Elite": ["Maximum interest benefits", "Completely flexible terms", "Zero penalty withdrawals"]
            },
            "Government & Corporate Bonds": {
                "Entry": ["Stable returns", "Government security", "Regular income option"],
                "Standard": ["Enhanced yield potential", "Diversified portfolio", "Tax-efficient structures"],
                "Premium": ["Strategic allocation", "Premium bond access", "Tailored maturity laddering"],
                "Elite": ["Maximum yield optimization", "Exclusive bond offerings", "Customized portfolio management"]
            },
            "REITs": {
                "Entry": ["Steady income stream", "Real estate exposure", "Liquidity advantages"],
                "Standard": ["Enhanced property diversification", "Higher income potential", "Professional management"],
                "Premium": ["Premium property portfolio", "Strategic sector allocation", "Inflation protection"],
                "Elite": ["Elite property holdings", "Maximum income generation", "Private REIT options"]
            },
            "ETFs": {
                "Entry": ["Market exposure", "Diversification benefits", "Low management fees"],
                "Standard": ["Enhanced sector allocation", "Dividend optimization", "Tax-efficient structure"],
                "Premium": ["Strategic multi-asset exposure", "Premium ETF access", "Portfolio rebalancing"],
                "Elite": ["Maximum diversification", "Exclusive ETF offerings", "Complete portfolio management"]
            }
        }
    }
    
    if category in descriptions and subcategory in descriptions[category] and tier in descriptions[category][subcategory]:
        description = descriptions[category][subcategory][tier]
    else:
        description = f"{tier.lower()} level {subcategory.lower()} {category.lower()} product for organizations."
        
    if category in benefits and subcategory in benefits[category] and tier in benefits[category][subcategory]:
        benefit_list = benefits[category][subcategory][tier]
    else:
        benefit_list = [f"{tier} level benefits for organizational customers"]
        
    return description, benefit_list

def main():
    products = generate_org_financial_products()
    
    
    with open('org_financial_products.json', 'w') as f:
        json.dump(products, f, indent=2)
    

if __name__ == "__main__":
    main()
