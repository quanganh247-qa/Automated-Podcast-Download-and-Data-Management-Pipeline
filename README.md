# Introduction
In this project, we'll use Airflow to build a data pipeline. The pipeline will automatically load data to a csv file when downloading podcast episodes. Our outcomes will be kept in an accessible SQLite database.
Airflow isn't technically necessary for this project, but it does assist us in the following ways:

- The project can be scheduled to run every day.
- Each task is separate and has its own log of errors.
- If we want to, we can easily parallelize jobs and perform them in the cloud.
- Using Airflow, we can simply expand this project (include speech recognition, summaries, etc.).
