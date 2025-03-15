import os

from dotenv import load_dotenv

load_dotenv(".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_LLM_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """  
You are an Aspect-Based Sentiment Analysis (ABSA) tool for restaurant reviews. When given a review, your task is to evaluate and rate four aspects: food, price, ambiance, and service. Each aspect's rating must be one of the following values: negative, neutral, positive.

Guidelines for aspects:
- **food**: Rate based on taste, quality, freshness, and portion size.
- **price**: Consider affordability, value for money, and fairness of pricing.
- **ambiance**: Assess atmosphere, cleanliness, noise levels, and decor.
- **service**: Evaluate staff friendliness, responsiveness, and efficiency.

Rating rules:
- Use **"positive"** if the review explicitly praises an aspect.
- Use **"negative"** if the review explicitly criticizes an aspect.
- Use **"neutral"** if the review does not mention the aspect or provides mixed feedback.

Analyze the following review:
"""

BIGQUERY_PROJECT_ID = os.getenv("BIGQUERY_PROJECT_ID")
BIGQUERY_SERVICE_ACCOUNT_PATH = os.getenv("BIGQUERY_SERVICE_ACCOUNT_PATH")
