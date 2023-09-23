# Introduction
In this project, we'll use Airflow to build a data pipeline. The pipeline will automatically load data to a csv file when downloading podcast episodes. Our outcomes will be kept in an accessible SQLite database.

Airflow isn't technically necessary for this project, but it does assist us in the following ways:

- The project can be scheduled to run every day.
- Each task is separate and has its own log of errors.
- If we want to, we can easily parallelize jobs and perform them in the cloud.
- Using Airflow, we can simply expand this project (include speech recognition, summaries, etc.).

By the end of this project, you'll have a good understanding of how to use Airflow, along with a practical project that you can continue to build on.

# Technically used
To follow this project, please install the following locally:

- Airflow 2.3+
- Python 3.8+
- Python packages:
  - pandas
  - sqlite3
  - xmltodict
  - requests
