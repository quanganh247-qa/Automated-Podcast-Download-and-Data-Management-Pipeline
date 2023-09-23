# Overview
This file describes, in order, the steps involved in doing this project.

## Step 1 : Prepare environent
- Recommend creating a virtualenv
- Install airflow
  - `pip install apache-airflow`
- Start terminal or other IDE
- Run airflow server in terminal
  - `airflow standalone`
- Edit airflow cfg to point to the folder with the dag you're writting
- Write first task in DAG

### Fisrt task :
```Python
import xmltodict
import requests
from airflow.decorators import dag, task
import pendulum

PODCAST_URL = "https://www.marketplace.org/feed/podcast/marketplace/"
@dag(
    dag_id = 'project_etl_podcast',
    description= 'Pdcast with Apache Airflow',
    start_date=days_ago(0),
    catchup= False,
)
def podcast_summary():
    @task
    def get_episodes():
        data = requests.get(PODCAST_URL)
        data_xml = xmltodict.parse(data.text)
        episodes = data_xml['rss']['channel']['item']
        print(f"This link have {len(episodes)} episodes")
        return episodes
    content_epi = get_episodes()
content = podcast()
```
