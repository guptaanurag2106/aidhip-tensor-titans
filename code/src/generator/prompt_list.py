def create_customer_persona_prompt(cust_count):
    return f"""
        Create {cust_count} detailed bank customer persona with the following attributes and only the following attributes:
        - age: Age (Range: Integer, typically 18-100)
        - gender: Gender (Type: String, Options: Male/Female/Other)
        - income: Income (Range: Integer, between 10,000 and 1,000,000)
        - education: Education (Type: String, Options: Primary/Secondary/Graduate)
        - is_married: Is Married (Type: Boolean)
        - num_of_children: Number of Children (Range: Integer, between 0 and 5)
        - location: Location (U.S.A. State)
        - job: Job/Career (Type: String)
        - goals: Goals (Type: Comma Separated String, The financial goals of the customer, stability/ high risk/retirement etc.)
        - credit_score: Credit Score (Range: Integer, typically 300-850)
        - preferred_payment_method: Preferred Payment Method (Type: String, Options: Credit Card/Debit Card/Cash/Online)
        - avg_balance: Average Past 12 Month Bank Balance (Type: Float/Integer)
        - loan_count: Number of Lifetime Loans (Range: Integer, 0 and above)
        - total_loan_amt: Total Loan Amount (Range: Float/Integer)
        - avg_monthly_spending: Average Monthly Spending (Type: Float/Integer)
        - main_purchase_cat: Main Purchase Categories (Comma Separated String)
        - support_interaction_count: Number of Lifetime Support Interactions (Range: Integer)
        The data should be congruent with itself and be representative of average U.S. population in the demographic
        Return the persona in a structured array of JSON format using the key mentioned after every field.
        """


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
    Financial Goals: {persona["goals"]}
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
    The transactions can be shopping for general stuff (based on their persona, family status, age etc.
    or investments, money transfers etc. based on their financial goals/income/family status etc.)
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
        return ""

    return f"""
    Generate maximum of {num_complaints} realistic customer support complaints to a popular U.S.A bank for the following bank customer:
    Age: {persona["age"]}
    Gender: {persona["gender"]}
    Income: {persona["income"]}
    Education: {persona["education"]}
    Is Married: {persona["is_married"]}
    Number of Children: {persona["num_of_children"]}
    Financial Goals: {persona["goals"]}
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
    sentiment = (
        "mostly positive"
        if persona["satisfaction"] >= 7
        else "mixed"
        if persona["satisfaction"] >= 4
        else "mostly negative"
    )

    return f"""
    Generate maximum of {num_posts} realistic social media posts (tweets) for the following bank customer:
    
    Age: {persona["age"]}
    Gender: {persona["gender"]}
    Income: {persona["income"]}
    Education: {persona["education"]}
    Is Married: {persona["is_married"]}
    Number of Children: {persona["num_of_children"]}
    Job/Career: {persona["job"]}
    Financial Goals: {persona["goals"]}
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
