def create_customer_persona_prompt(cust_count):
    return f"""
        Create {cust_count} detailed bank customer persona with the following attributes and only the following attributes for a particular U.S. bank:
        - age: Age (Range: Integer, typically 18-100)
        - gender: Gender (Type: String, Options: Male/Female/Other)
        - education: Education (Type: String, Options: Primary/Secondary/Graduate)
        - is_married: Is Married (Type: Boolean)
        - num_of_children: Number of Children (Range: Integer, between 0 and 5)
        - location: Location (U.S.A. State)
        - income: Income (Range: Integer, between 0 (say for non-working students) and 1,000,000)
        - job: Job/Career (Type: String, can even be a student)
        - goals: Goals (Type: Comma Separated String, The financial goals of the customer, stability/ high risk/retirement etc.)
        - credit_score: Credit Score (Range: Integer, typically 300-850)
        - preferred_payment_method: Preferred Payment Method (Type: String, Options: Credit Card/Debit Card/Cash/Online)
        - balance: Comma separated list of past 12 Month Bank Balance (Type: Comma separated list of float, older to newer)
        - loan_amts: Comma separated list of Loan Amount (Type: Comma separated list of float, older to newer)
        - monthly_spending: Average Monthly Spending (from this bank) (Type: Comma separated list of Float/Integer, older to newer)
        - main_purchase_cat: Main Purchase Categories (Comma Separated String)
        - support_interaction_count: Number of Lifetime Customer Support Interactions, could be for asking for products, complaining etc. (Range: Integer)
        - satisfaction: Customer's satisfaction with the bank, average is around 7 but could be lower or higher (Type: Float 0-10)

        The data should be congruent with itself and be representative of average U.S. population in the demographic
        The trend in list of bank balance, loan amounts, and monthly_spending (from this bank's account) over time could show changes in persons income over time,
        or maybe person is withdrawing money from bank showing decreasing trust (satisfaction) in bank, or increasing/decreasing monthly_spending without
        changes in income/loan could show shift from/to another bank account showing their satisfaction level with the bank.
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
    List of past 12 Month Bank Balance (older to newer): {persona["balance"]}
    List of past 12 Month Loan Amounts (older to newer): {persona["loan_amts"]}
    List of past 12 Month Spending (older to newer): {persona["monthly_spending"]}
    Main Purchase Categories: {persona["main_purchase_cat"]}
    Number of Lifetime Support Interactions: {persona["support_interaction_count"]}
    Satisfaction: {persona["satisfaction"]}/10, Customer's satisfaction with the bank, lower satisfaction could imply lesser new transactions
    
    From these info about the customer using their preferred_payment_method (not always the same),
    there income, categories generate the following data (It can have some outliers but most should follow the customer info),
    Also make sure the Monthly Spending matches with the transactions created
    The transactions can be shopping for general stuff (based on their persona, family status, age etc.
    or investments, money transfers etc. based on their financial goals/income/family status etc.)
    Transactions could have increasing/decreasing trend over time based on increasing or decreasing loans, bank balance satisfaction with bank
    Customers could have taken out loans for rent / education / low bank balance
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
    Job/Career: {persona["job"]}
    Financial Goals: {persona["goals"]}
    Credit Score: {persona["credit_score"]}
    Preferred Payment Method: {persona["preferred_payment_method"]}
    Location: {persona["location"]}
    List of past 12 Month Bank Balance (older to newer): {persona["balance"]}
    List of past 12 Month Loan Amounts (older to newer): {persona["loan_amts"]}
    List of past 12 Month Spending (older to newer): {persona["monthly_spending"]}
    Main Purchase Categories: {persona["main_purchase_cat"]}
    Number of Lifetime Support Interactions: {persona["support_interaction_count"]}
    Satisfaction: {persona["satisfaction"]}/10, Customer's satisfaction with the bank, lower satisfaction could imply lesser new transactions
    
    Each complaint should include the following and only these attributes:
    date: Date (Format: DD/MM/YYYY should be in past 1 year)
    transcript: Transcript (Type: String, Max: 150 words, Text: Full transcript of the conversation)
    main_concerns: Main Concerns (Type: String, Example: "Billing issue", "Technical support")
    is_repeating_issue: Is Repeating Issue (Type: Boolean, True/False)
    was_issue_resolved: Was Issue Resolved (Type: Boolean, True/False, a lot of simpler issues, or issues inquiring about products are usually solved)
    sentiment: Sentiment (Type: Double, Options: -1 to 1)
    
    Return the complaints as a JSON array.
    """


def create_social_media_prompt(persona, num_posts):
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
    List of past 12 Month Bank Balance (older to newer): {persona["balance"]}
    List of past 12 Month Loan Amounts (older to newer): {persona["loan_amts"]}
    List of past 12 Month Spending (older to newer): {persona["monthly_spending"]}
    Main Purchase Categories: {persona["main_purchase_cat"]}
    Number of Lifetime Support Interactions: {persona["support_interaction_count"]}
    Satisfaction: {persona["satisfaction"]}/10, Customer's satisfaction with the bank, lower satisfaction could imply lesser new transactions
    
    The posts should be a mix of general life posts and occasionally banking-related posts.
    The banking-related sentiment should be {persona["satisfaction"]}/10 based on their satisfaction level.
    Each post should include the following and only these attributes:

    date: Date (Format: DD/MM/YY should be in past 1 year)
    platform: Platform (Options: 'Online', 'Offline')
    image_url: Image URL (Type: String, Example: 'https://example.com/images/abcd1234.jpg')
    text_content: Text Content (Type: String, Example: 'This is some text content about a product or service.')
    influencers_followed: Influencers Followed (Range: Integer, 0-10)
    topics_of_interest: Topics of Interest (Type: Comma separated String, Example: 'Technology,Sports,Finance')
    feedback_on_financial_products: Feedback on Financial Products (Options: 'Positive', 'Negative', 'Neutral')
    sentiment_score: Sentiment Score toward the bank/financial related topics(Range: Float, 0.0 to 10.0, Example: 7.4)
    engagement_level: Engagement Level (Range: Float, 0.0 to 10.0, Example: 6.2)
    brands_liked: Brands Liked (Type: Comma separated String, Example: 'Nike,Apple,Tesla'])
    
    Return the posts as a JSON array.
    """
