# Overview
This file describes, in order, the steps involved in doing this project.

## Prepare environent
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
## Create database
- Create database
- Run `sqlite3 episodes.db`
- Type `.databases` in prompt to create the db
- Run `airflow connections add 'podcasts' --conn-type 'sqlite' --conn-host 'episodes.db'`
- `airflow connections get podcasts` to view connection info
- Write second task

### Second task

```Python
create_dtb = SqliteOperator(
        task_id = 'create table ',
        sql = r"""
        create table if no exist episodes(
            link text primary key,
            title text,
            name text,
            published text,
            description text,
            transcript text,
        );""",
        sqlite_conn_id= 'podcasts',
    )
```
- Trigger run
- Show in GUI

## Load episodes into SQLite
- `pip install 'apache-airflow[pandas]'`
- Add in load episodes function

```Python
 @task 
    def load_content(episodes):
        hook = SqliteHook(sqlite_conn_id ='podcasts')
        episodes_container = hook.get_pandas_df("select * from episodes ;")
        new_container = []
        for e in episodes:
            if e['link'] not in episodes_container['link']:
                name = f"{e['link'].split('/')[-2]}.mp3"
                new_container.append(e['link'],e['title'],e['published'],e['description'],e['transcript'],name)
        hook.insert_rows(table='episodes',rows=new_container,target_fields=["link", "title", "published", "description", "name"])
        return new_container
    
    new_container = load_content(content_epi)
```

## Third task
```Pyton
import requests
import xmltodict
from airflow.decorators import dag, task
import pendulum
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook

PODCAST_URL = "https://www.marketplace.org/feed/podcast/marketplace/"

@dag(
    dag_id = 'project_etl_podcast',
    description= 'Pdcast with Apache Airflow',
    start_date=days_ago(0),
    catchup= False,
)

def podcast():
    create_dtb = SqliteOperator(
        task_id = 'create table ',
        sql = r"""
        create table if no exist episodes(
            link text primary key,
            title text,
            name text,
            published text,
            description text,
            transcript text,
        );""",
        sqlite_conn_id= 'podcasts',
    )

    @task
    def get_episodes():
        data = requests.get(PODCAST_URL)
        data_xml = xmltodict.parse(data.text)
        episodes = data_xml['rss']['channel']['item']
        print(f"This link have {len(episodes)} episodes")
        return episodes

    content_epi = get_episodes()
    create_dtb.set_downstream(content_epi)

    @task 
    def load_content(episodes):
        hook = SqliteHook(sqlite_conn_id ='podcasts')
        episodes_container = hook.get_pandas_df("select * from episodes ;")
        new_container = []
        for e in episodes:
            if e['link'] not in episodes_container['link']:
                name = f"{e['link'].split('/')[-2]}.mp3"
                new_container.append(e['link'],e['title'],e['published'],e['description'],e['transcript'],name)
        hook.insert_rows(table='episodes',rows=new_container,target_fields=["link", "title", "published", "description", "name"])
        return new_container
    
    new_container = load_content(content_epi)
```
- Trigger run
- Show in GUI
- View database
    - `sqlite3 episodes.db`
## Load into csv and download
```Python
@task
    def download(episodes):
        new_episodes = []
        for episode in episodes:
            data = dict(link =episode["link"],
                title = episode["title"],
                pubDate = episode["pubDate"],
                description = episode["description"],
                filename = episode["link"].split('/')[-1]
                )
            new_episodes.append(data)
        df= pd.DataFrame(new_episodes)
        df.to_csv("data.csv")
        return new_episodes
    download(content_epi)
```
- Trigger task
- Show in GUI
- View files in folder where is project located

