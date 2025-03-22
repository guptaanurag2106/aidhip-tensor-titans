def create_org_persona_prompt(org_count):
    return f"""
        Create {org_count} detailed bank corporate customer personas with the following attributes and only the following attributes:
        - company_name: Company Name (Type: String)
        - industry: Industry (Type: String, Examples: Technology, Healthcare, Finance, Manufacturing, Retail, etc.)
        - size: Company Size (Type: String, Examples: Small (1-50), Medium (51-250), Large (251-1000), Enterprise (1000+))
        - annual_revenue: Annual Revenue (Range: Integer, between 100,000 and 500,000,000)
        - years_in_business: Years in Business (Range: Integer, between 1 and 100)
        - location: Location (U.S.A. State)
        - business_model: Business Model (Type: String, Examples: B2B, B2C, Hybrid)
        - growth_stage: Growth Stage (Type: String, Examples: Startup, Growth, Mature, Declining)
        - risk_tolerance: Risk Tolerance (Type: String, Options: Low/Medium/High)
        - credit_rating: Credit Rating (Type: String, Examples: AAA, AA, A, BBB, BB, B)
        - preferred_payment_method: Preferred Payment Method (Type: String, Options: Wire Transfer/ACH/Credit Card/Check)
        - avg_account_balance: Average Past 12 Month Bank Balance (Type: Float/Integer)
        - loan_count: Number of Lifetime Loans (Range: Integer, 0 and above)
        - total_loan_amt: Total Loan Amount (Range: Float/Integer)
        - avg_monthly_spending: Average Monthly Spending (Type: Float/Integer)
        - main_expense_categories: Main Expense Categories (Comma Separated String)
        - support_interaction_count: Number of Lifetime Support Interactions (Range: Integer)
        
        The data should be congruent with itself and be representative of average U.S. businesses in different sectors.
        Return the persona in a structured array of JSON format using the key mentioned after every field.
        """


def create_org_transaction_history_prompt(persona, num_transactions):
    return f"""
    Generate between 1 and {num_transactions} realistic corporate bank transactions for the following organization:
    Company Name: {persona["company_name"]}
    Industry: {persona["industry"]}
    Company Size: {persona["size"]}
    Annual Revenue: {persona["annual_revenue"]}
    Years in Business: {persona["years_in_business"]}
    Location: {persona["location"]}
    Business Model: {persona["business_model"]}
    Growth Stage: {persona["growth_stage"]}
    Risk Tolerance: {persona["risk_tolerance"]}
    Credit Rating: {persona["credit_rating"]}
    Preferred Payment Method: {persona["preferred_payment_method"]}
    Average Account Balance: {persona["avg_account_balance"]}
    Number of Lifetime Loans: {persona["loan_count"]}
    Total Loan Amount: {persona["total_loan_amt"]}
    Average Monthly Spending: {persona["avg_monthly_spending"]}
    Main Expense Categories: {persona["main_expense_categories"]}
    
    From this information about the organization, using their preferred_payment_method (not always the same),
    their revenue, and expense categories, generate the following data (It can have some outliers but most should follow the organization's profile).
    Also, make sure the Average Monthly Spending matches with the transactions created.
    
    The transactions should include corporate expenses like payroll, vendor payments, equipment purchases, 
    service subscriptions, loan payments, etc. based on their industry, size, and business model.
    
    Each transaction should include these and only these attributes:

    date: Date (Format: DD/MM/YYYY should be within last year)
    platform: Platform (Type: String, Options: Online/Bank Transfer/Vendor Portal/ERP System etc.)
    payment_method: Payment Method (Options: Wire Transfer/ACH/Credit Card/Check/Direct Deposit)
    amount: Amount (Type: Float, Example: 10000.00)
    location: Location (Type: String, Example: State or "Remote")
    expense_category: Expense Category (Type: String, Example: Payroll, Marketing, Equipment, etc.)
    expense_sub_category: Expense Sub Category (Type: String, Example: Salaries, Digital Ads, Computers, etc.)
    vendor: Vendor (Type: String, Example: ADP, Google, Dell, etc.)
    transaction_type: Transaction Type (Type: String, Options: Payment/Deposit/Transfer/Loan/Investment)
    
    Return the transactions as a JSON array.
    """


def create_org_support_prompt(persona, num_support):
    if num_support == 0:
        return ""

    return f"""
    Generate maximum of {num_support} realistic corporate banking support tickets for the following organization:
    Company Name: {persona["company_name"]}
    Industry: {persona["industry"]}
    Company Size: {persona["size"]}
    Annual Revenue: {persona["annual_revenue"]}
    Years in Business: {persona["years_in_business"]}
    Location: {persona["location"]}
    Business Model: {persona["business_model"]}
    Growth Stage: {persona["growth_stage"]}
    Risk Tolerance: {persona["risk_tolerance"]}
    Credit Rating: {persona["credit_rating"]}
    Preferred Payment Method: {persona["preferred_payment_method"]}
    Average Account Balance: {persona["avg_account_balance"]}
    Number of Lifetime Loans: {persona["loan_count"]}
    Total Loan Amount: {persona["total_loan_amt"]}
    Average Monthly Spending: {persona["avg_monthly_spending"]}
    Main Expense Categories: {persona["main_expense_categories"]}
    Support Interaction Count: {persona["support_interaction_count"]}
    Satisfaction with bank: {persona["satisfaction"]}/10
    
    Each support ticket should include the following and only these attributes:
    date: Date (Format: DD/MM/YYYY should be in past 1 year)
    transcript: Transcript (Type: String, Max: 200 words, Text: Full transcript of the conversation between the organization's representative and bank support)
    issue_type: Issue Type (Type: String, Example: "Payment Processing Issue", "Loan Application", "Technical Support", "Fraud Alert")
    priority: Priority (Type: String, Options: Low/Medium/High/Critical)
    is_repeating_issue: Is Repeating Issue (Type: Boolean, True/False)
    was_issue_resolved: Was Issue Resolved (Type: Boolean, True/False)
    resolution_time: Resolution Time (Type: String, Example: "4 hours", "3 days", "Not resolved")
    sentiment: Sentiment (Type: Double, Options: -1 to 1)
    
    Make sure the support tickets reflect realistic corporate banking issues that would be appropriate for the organization's profile.
    Include a mix of questions, complaints, service requests, and general inquiries.
    The support issues should be more formal and business-oriented than individual customer issues.
    
    Return the support tickets as a JSON array.
    """


def create_org_social_media_prompt(persona, num_posts):
    sentiment = (
        "mostly positive"
        if persona["satisfaction"] >= 7
        else "mixed"
        if persona["satisfaction"] >= 4
        else "mostly negative"
    )

    return f"""
    Generate maximum of {num_posts} realistic corporate social media posts for the following organization:
    
    Company Name: {persona["company_name"]}
    Industry: {persona["industry"]}
    Company Size: {persona["size"]}
    Annual Revenue: {persona["annual_revenue"]}
    Years in Business: {persona["years_in_business"]}
    Location: {persona["location"]}
    Business Model: {persona["business_model"]}
    Growth Stage: {persona["growth_stage"]}
    Risk Tolerance: {persona["risk_tolerance"]}
    Credit Rating: {persona["credit_rating"]}
    Satisfaction with bank: {persona["satisfaction"]}/10
    
    The posts should include a mix of company announcements, industry news, product/service promotions, 
    partnerships, and occasionally banking or financial service-related content.
    
    The banking-related sentiment should be {sentiment} based on their satisfaction level.
    The posts should be professional and aligned with the organization's industry and business model.
    
    Each post should include the following and only these attributes:

    date: Date (Format: DD/MM/YY should be in past 1 year)
    platform: Platform (Options: 'LinkedIn', 'Twitter', 'Facebook', 'Instagram', 'Company Blog')
    image_url: Image URL (Type: String, Example: 'https://example.com/images/corporate/abcd1234.jpg')
    text_content: Text Content (Type: String, Max: 280 characters for Twitter, longer for other platforms)
    topics_of_interest: Topics of Interest (Type: List of Strings, Example: ['Industry News', 'Technology Trends', 'Finance', 'Sustainability'])
    feedback_on_financial_services: Feedback on Financial Services (Options: 'Positive', 'Negative', 'Neutral', 'Not Applicable')
    sentiment_score: Sentiment Score (Range: Float, 0.0 to 10.0, Example: 7.4)
    engagement_level: Engagement Level (Range: Float, 0.0 to 10.0, Example: 6.2)
    partners_mentioned: Partners Mentioned (Type: List of Strings, Example: ['Microsoft', 'Salesforce', 'Local Chamber of Commerce'])
    post_type: Post Type (Type: String, Options: 'Announcement', 'Promotion', 'Industry News', 'Financial', 'Community', 'Hiring')
    
    Return the posts as a JSON array.
    """
