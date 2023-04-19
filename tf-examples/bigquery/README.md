# Google BigQuea

BigQuery is data warehouse solution from Google.

To add sample dataset in order to play with Bigquery, from the console, BigQuery UI, click ADD DATA in the middle of the screen. Here, you can add data from Local file, GCS bucket, Amazon or Azure Storage or even Google Drive files. There are built-in public datasets available which can be accessed by clicking on *Public Datasets*. Next choose the datasets of your choice, in our case, let's search for `education` datasets and click *International Education*, click View Datasets and those get added into your account. Below are some of the features of BigQuery.

- BigQuery ML for machine learning
- BigQuery allows to query different data sources (SQL, other cloud providers)
- Realtime analytics with built-in query acceleration using BI engine.
- This also supports geospatial data.

BigQuery also comes with many of the [migration API](https://cloud.google.com/bigquery/docs/batch-sql-translator) which will translate existing queries in different dialect to BigQuery specific queries. There is also [interactive translator](https://cloud.google.com/bigquery/docs/interactive-sql-translator) for converting queries interactively.

In BigQuery, datasets are located in specific geography and all the tables in that dataset must be located in the same geographic location. If you want to move data into a dataset, the source and target datasets must reside in the same location. The dataset access is controlled using IAM. To add permission to a dataset, click on the three dots >> Share >> ADD PRINCIPAL and specify the email address of the person whom you want to provide access and then specify the built in role. Just like Presto, we can also connect to other SQL data sources like MySQL [using connections](https://cloud.google.com/bigquery/docs/connect-to-sql). We can send REST request to perform certain action on Bigquery just like any other service on GCP.

BigQuery also performs some query caching so that same query should return cached results next time we run. The [cached query results](https://cloud.google.com/bigquery/docs/cached-results) work per user per project. BigQuery is also strange that it doesn't need denormalized schema in order to get good performance. In fact, GCP documentation encourages [nested and repeated fields](https://cloud.google.com/bigquery/docs/best-practices-performance-nested) for denormalization. BigQuery supports access control at dataset. tanble, column and row level.

Now, those can be accessed under `bigquery-public-data`. From the UI, we can click on the PREVIEW tab to see some sample data. This is better than `SELECT * FROM <table>` because this does not incur any charges on BigQuery. There are tables for SCHEMA, DETAILS as well which will show partitioninig and clustering information if any. When we click on *Query*, it will populate general query in the editor on browser. We can use `Ctrl + Space` to auto fill column and table information. The table name is specified as `<project_id>.<dataset>.<table_name>` format. Querying by using partition key is always better than without those as filter columns. Also, this is stored in columnar data format so always query only the columns you need and not everything using `SELECT *`. `world_bank_intl_education` dataset has some smaller tables to experiment with.

Some SQL scripts would contain `#standardSQL` at the top which would make sure that we are using a SQL dialect which is compatible with standard SQL.

## Pricing Options

1. **On-demand pricing** is like cost based on how much data we query. This is the default model of pricing on BigQuery. First 1TB data querying is free. With this model, there is maximum 2000 concurrent slots per project. So, for large companies, this model may not be good because it will throttle the capacity with 2000 slots. Cancelling a running query might incur costs of full query. When querying clustered table with clustered column included in the filter, if we include `LIMIT` clause, it will prune the blocks scanned for getting results and reduce costs. The costs are 5$ per TB of data queried.
2. **Capacity-compute Pricing**: This is for setting predictable costs for a project. In this case, we reserve BigQuery slots for certain period of time and offers pay as go model with autoscaling. This is available in three tiers; Standard, Enterprise, Enterprise Plus. This also applies to BI Engine costs, BigQuery ML and does not incur any storage costs.
     **Flat-rate pricing** is more suitable for large teams. If we give annual commitment then we get better pricing. When enrolled in capacity pricing, we purchase bigquery slots. So, when querying, we consume these slots and we are not charged for storage. This has minimum 100 slots and can be purchased in multiples of 100. We can go with monthly or annual commitment.

## Cost Optimization

1. Do not use `SELECT *` on the table. You can verify this information by checking the `bigquery-public-data.geo_openstreetmap` dataset which is large. Querying full table will show in validator that its going to consume so much GBs and if we query only single column, it would not charge so much.
2. Always partition your data. Partitioning is possible only on DATE, DATETIME or TIMESTAMP fields for column partitions or we can use RANGE PARTITIONING for INTEGER columns which has limit of 10000 maximum partitions. So, RANGE PARTITIONING cannot exceed more than 10000 partitions. For small tables, do not worry so much about partitioning or optimization because developer time costs more than BigQuery costs.
3. Try to cluster your table. This will at least give better performance than normal only partitioned tables.
4. `LIMIT` clause does not reduce cost for data warehouse engines. So, it will not impact the costs. Clustered tables can reduce cost with `LIMIT` clause.
5. Materialize query results in stages. This is similar to having multiple stages of data tables which are improved in quality like different layers of tables(raw, bronze, silver, gold).

The quota can be limited on project level using Query Usage Per day quota. If it goes over that, the queries would start failing but you will not be charged surprise bill. Similarly, there is Query usage Per Day per User quota is also useful. There are ways to set up [custom cost quotas](https://cloud.google.com/bigquery/docs/custom-quotas) to reduce querying costs.