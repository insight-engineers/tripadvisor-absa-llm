from absa.constants import BIGQUERY_PROJECT_ID, BIGQUERY_SERVICE_ACCOUNT_PATH
from absa.handler.bigquery import BigQueryHandler
from absa.utils.functions import initialize_openai, process_absa_table
from datetime import datetime

bigquery_client = BigQueryHandler(
    project_id=BIGQUERY_PROJECT_ID, credentials_path=BIGQUERY_SERVICE_ACCOUNT_PATH
)


def process_and_append_new_reviews():
    """
    Process reviews using ABSA and append only new review_ids to dim_review_absa.
    """
    # Fetch existing reviews and processed reviews
    original_reviews = bigquery_client.fetch_bigquery(
        "SELECT * FROM `tripadvisor-recommendations.dm_tripadvisor.dim_review`"
    )

    try:
        existing_review_ids = bigquery_client.fetch_bigquery(
            "SELECT DISTINCT review_id FROM `tripadvisor-recommendations.dm_tripadvisor.dim_review_absa`"
        )
        existing_review_ids = existing_review_ids["review_id"].tolist()
        print(f"Found {len(existing_review_ids)} existing reviews.")
    except:
        existing_review_ids = []
        print("No existing reviews found.")

    # Filter out already processed reviews
    new_reviews = original_reviews[
        ~original_reviews["review_id"].isin(existing_review_ids)
    ]

    if new_reviews.empty:
        print("No new reviews to process.")
        return

    print(f"Process {len(new_reviews)} new reviews.")
    # Process new reviews
    openai_client = initialize_openai()
    processed_reviews = process_absa_table(
        client=openai_client,
        df=new_reviews,
        review_cols=["review_title", "review_description"],
    )

    print(f"Succesfully processed {len(processed_reviews)} reviews.")
    parquet_file_path = (
        f"data/absa_result_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.parquet"
    )
    processed_reviews.to_parquet(parquet_file_path, index=False)

    # Append new processed reviews to dim_review_absa
    bigquery_client.upload_parquet_to_bq(
        file_path=parquet_file_path,
        full_table_id="tripadvisor-recommendations.dm_tripadvisor.dim_review_absa",
        write_disposition="WRITE_APPEND",
    )

    print("New reviews processed and appended successfully.")


if __name__ == "__main__":
    process_and_append_new_reviews()
