import os

from dotenv import load_dotenv

load_dotenv(".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_LLM_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """  
You are an Aspect-Based Sentiment Analysis (ABSA) tool for restaurant aspects. When given a review, your task is to evaluate and rate four aspects: food, price, ambiance, and service. Each aspect's rating must be one of the following values: negative, neutral, positive.

Guidelines for aspects:
- **general**: Provide an overall rating based on the review's sentiment.
- **food**: Rate based on taste, quality, freshness, and portion size.
- **price**: Consider affordability, value for money, and fairness of pricing.
- **ambiance**: Assess atmosphere, cleanliness, noise levels, and decor.
- **service**: Evaluate staff friendliness, responsiveness, and efficiency.
- **location**: Rate based on nearby attractions, accessibility, and parking.

Rating rules:
- Use positive if the aspect explicitly praises an aspect.
- Use negative if the aspect explicitly criticizes an aspect.
- Use neutral if the aspect provides mixed feedback or presents facts without opinion.
- Use not_given if the aspect is not mentioned.
"""

BIGQUERY_PROJECT_ID = os.getenv("BIGQUERY_PROJECT_ID")
BIGQUERY_SERVICE_ACCOUNT_PATH = os.getenv("BIGQUERY_SERVICE_ACCOUNT_PATH")
