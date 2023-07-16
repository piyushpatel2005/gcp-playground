from google.cloud import bigquery
import pathlib



def query_stackoverflow():
    """
    Query a dataset. Required permissions BigQuery Data Editor and BigQuery Job User to submit query job.
    """
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT
          CONCAT(
            'https://stackoverflow.com/questions/',
            CAST(id as STRING)) as url,
          view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags like '%google-bigquery%'
        ORDER BY view_count DESC
        LIMIT 10"""
    )

    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print("{} : {} views".format(row.url, row.view_count))

def create_dataset():
    """
    Create dataset in specified region.
    When default_project is not set dataset_id must be fully-qualified dataset ID with 'project_id.dataset_id'"""
    project = 'concise-kayak-389317'
    # client = bigquery.Client()
    client = bigquery.Client(project=project)


    dataset_id = 'ran_expl'
    # TODO(developer): Set dataset_id to the ID of the dataset to create.
    dataset_id = "{}.{}".format(client.project, dataset_id)

    # Construct a full Dataset object to send to the API.
    dataset = bigquery.Dataset(dataset_id)

    # TODO(developer): Specify the geographic location where the dataset should reside.
    dataset.location = "US"

    # Send the dataset to the API for creation, with an explicit timeout.
    # Raises google.api_core.exceptions.Conflict if the Dataset already
    # exists within the project.
    dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

def create_table_from_json_schema(dataset_id, table_id: str) -> None:
    orig_table_id = table_id
    current_directory = pathlib.Path(__file__).parent
    orig_schema_path = str(current_directory / "schemas/schema.json")

    client = bigquery.Client()

    # TODO(dev): Change table_id to the full name of the table you want to create.
    table_id = f"{client.project}.{dataset_id}.{table_id}"
    # TODO(dev): Change schema_path variable to the path of your schema file.
    schema_path = "path/to/schema.json"
    # [END bigquery_schema_file_create]
    # table_id = orig_table_id
    schema_path = orig_schema_path

    # [START bigquery_schema_file_create]
    # To load a schema file use the schema_from_json method.
    schema = client.schema_from_json(schema_path)
    print(schema)

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # API request
    print(f"Created table {table_id}.")
  


if __name__ == "__main__":
    # query_stackoverflow()
    # create_dataset()
    create_table_from_json_schema('ran_expl', 'sales')