from typing import Dict, List

import openai
import pandas as pd

from absa.constants import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_LLM_MODEL,
    SYSTEM_PROMPT,
)
from absa.utils.models import AspectRating

from collections import OrderedDict


def initialize_openai():
    return openai.OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)


def process_absa(client, review_message: str) -> Dict[str, str]:
    try:
        if review_message.startswith("Not Defined."):
            raise Exception("The review message is not defined.")

        if not review_message or review_message.isspace() or review_message.isnumeric():
            raise Exception("The review message is not valid.")

        # process for avoid repeated sentences

        review_message = ". ".join(OrderedDict.fromkeys(review_message.split(". ")))

        completion = client.beta.chat.completions.parse(
            model=OPENAI_LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": review_message},
            ],
            temperature=0.1,
            top_p=1,
            response_format=AspectRating,
        )

        if completion.choices[0].message.parsed:
            print(f"OUTPUT: {completion.choices[0].message.parsed}")
            return (completion.choices[0].message.parsed).model_dump()
        elif completion.choices[0].message.refusal:
            print(f"REFUSAL: {completion.choices[0].message.refusal}")
            raise ValueError(completion.choices[0].message.refusal)
        else:
            raise ValueError("No response from the model. Check billing.")

    except Exception as e:
        print(f"An error occurred: {e}")
        return AspectRating(
            food="neutral", price="neutral", ambience="neutral", service="neutral"
        ).model_dump()
    except ValueError as e:
        raise Exception(
            f"Refusal error occurred for the review message: {review_message}."
            f"Error: {e}"
        )


def process_absa_table(
    client, df: pd.DataFrame, review_cols: List[str] = None
) -> pd.DataFrame:
    """
    Return a DataFrame with the aspect ratings for each review in the input DataFrame.
    Create 4 new columns in the output DataFrame: food, price, ambience, and service.
    """
    processed_df = pd.DataFrame(columns=df.columns)
    original_df = df.copy()
    if review_cols is None:
        raise ValueError("The review column is required.")

    try:
        for index, row in original_df.iterrows():
            print("Processing review:", row["review_id"])
            connector = ". " if len(review_cols) > 1 else ""
            review = connector.join([row[col] for col in review_cols])
            aspect_ratings = process_absa(client, review)

            original_df.loc[index, "food"] = aspect_ratings["food"]
            original_df.loc[index, "price"] = aspect_ratings["price"]
            original_df.loc[index, "ambience"] = aspect_ratings["ambience"]
            original_df.loc[index, "service"] = aspect_ratings["service"]

            # add the processed review to the processed_df
            processed_df = pd.concat([processed_df, original_df.loc[[index]]])

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return processed_df
