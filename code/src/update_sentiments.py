from utils import send_request
import json


def update_support_history(data: dict) -> str:
    # update sentiment
    prompt = f"""
        Given a customer support query {data} to a major U.S. bank, give the sentiment value
        -1 means very negative comment/sentiment towards the bank by the customer
        1 means a very positive comment/sentiment
        0 means a neutral comment (Could be a person inquiring for a bank feature or a simple question)

        Return only the sentiment value (Type: Float) as a string, do not return anything else
        example return "0.1"
    """
    response = send_request(prompt)

    sentiment = "0"

    if response.status_code == 200:
        response_data = response.json()
        sentiment = response_data["choices"][0]["message"]["content"]

    return sentiment


def update_social_media_history(data: dict) -> dict:
    # update sentiment
    prompt = f"""
        Given a customer's social media message {data}, give the sentiment_score 
        -1 means very negative comment/sentiment towards the bank by the customer
        1 means a very positive comment/sentiment
        0 means a neutral comment (Possibly not related to financial topic)

        sentiment_score: Sentiment Score (Type: String, between -1 to 1)
        engagement_level: Engagement level towards the bank (Type: String, between -1(No engagement) to 1(Engagement))
        brands_liked: Brands Liked or talked about in the post (Type: Comma separated string of brand names)
        
        Return the transactions as a JSON array.
    """
    response = send_request(prompt)

    output = {"sentiment_score": "", "engagement_level": "", "brands_liked": 0}

    if response.status_code == 200:
        response_data = response.json()
        response_text = response_data["choices"][0]["message"]["content"]
        try:
            response_text = response_text.strip().lstrip("```json").rstrip("```")

            response_data = json.loads(response_text)

            print(response_data)
            output["sentiment_score"] = response_data["sentiment_score"]
            output["engagement_level"] = response_data["engagement_level"]
            output["brands_liked"] = response_data["brands_liked"]
        except:
            print("Could not parse JSON from response:", response_data)

    return output
