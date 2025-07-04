import pandas as pd
import sqlparse
from google.api_core.exceptions import GoogleAPIError
from google.cloud import bigquery
from google.oauth2.service_account import Credentials


class BigQueryHandler:
    """
    BigQueryHandler for interacting with BigQuery, including table management, data upload, and fetching queries.
    """

    def __init__(self, project_id: str, credentials_path: str = None):
        """
        Initialize the BigQueryHandler with a specified project and dataset.

        Args:
            project_id (str): GCP project ID.
            credentials_path (str): Path to the service account JSON file.
        """
        if not project_id:
            raise ValueError("Project ID is required to initialize BigQueryHandler.")

        if not credentials_path:
            raise ValueError("Please provide a path to the service account JSON file")

        self.project_id = project_id
        self.client = bigquery.Client(
            credentials=Credentials.from_service_account_file(credentials_path),
            project=self.project_id,
        )

        print(f"Initialized BigQueryHandler for project: {project_id}")

    def normalize_query(self, query: str) -> str:
        """
        Normalize a BigQuery query
        E.g: Remove ; at the end or comments

        Args:
            query (str): The query to normalize.
        """
        _query = query.strip().rstrip(";")
        _query = sqlparse.format(
            _query,
            reindent=True,
            strip_comments=True,
            strip_whitespace=True,
            keyword_case="upper",
        )

        print(f"Normalized query:\n{_query}")
        return _query

    def fetch_bigquery(self, query: str) -> pd.DataFrame:
        """
        Execute a query on a BigQuery table and return the results as a DataFrame.

        Args:
            query (str): The query to execute on the BigQuery table.

        Returns:
            pd.DataFrame: DataFrame containing the query results.
        """
        try:
            _query = self.normalize_query(query)
            dataframe = self.client.query(_query).to_dataframe()

            return pd.DataFrame(dataframe)

        except GoogleAPIError as api_error:
            print(f"Google API Error during data fetch: {api_error}")
            raise

        except Exception as e:
            print(f"An unexpected error occurred during data fetch.")
            raise

    def upload_parquet_to_bq(
        self, file_path: str, full_table_id: str, write_disposition="WRITE_TRUNCATE"
    ) -> None:
        """
        Upload a Parquet file to a specified BigQuery table.

        Args:
            file_path (str): Path to the Parquet file to upload.
            full_table_id (str): The table name where the data will be uploaded.
            write_disposition (str): Defines the write behavior when data already exists.
                                        Options: 'WRITE_TRUNCATE', 'WRITE_APPEND', 'WRITE_EMPTY'.
                                        Default: 'WRITE_TRUNCATE'.
        """
        try:
            print(
                f"Starting upload of Parquet file '{file_path}' to BigQuery table '{full_table_id}'"
            )

            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.PARQUET,
                write_disposition=write_disposition,
            )

            with open(file_path, "rb") as file:
                load_job = self.client.load_table_from_file(
                    file, full_table_id, job_config=job_config
                )

            load_job.result()  # Wait for the job to complete.
            print(
                f"Successfully uploaded file '{file_path}' to table '{full_table_id}'. Rows loaded: {load_job.output_rows}"
            )

        except FileNotFoundError as fnf_error:
            print(f"File not found: {fnf_error}")
            raise
        except GoogleAPIError as api_error:
            print(f"Google API Error during file upload: {api_error}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred during file upload.")
            raise

    def create_table(self, full_table_id: str, schema: list) -> None:
        """
        Creates a BigQuery table with a specified schema.

        Args:
            full_table_id (str): The table name to create.
            schema (list): List of bigquery.SchemaField objects defining the table schema.
        """
        try:
            print(f"Creating table '{full_table_id}' with schema: {schema}")

            table = bigquery.Table(full_table_id, schema=schema)
            table = self.client.create_table(table)

            print(f"Created table '{full_table_id}'")

        except GoogleAPIError as api_error:
            print(f"Google API Error during table creation: {api_error}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred during table creation.")
            raise
