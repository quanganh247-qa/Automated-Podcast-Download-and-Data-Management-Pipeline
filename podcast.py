import os
import json
import requests
import xmltodict
import pandas as pd
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task
import pendulum
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook

from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

PODCAST_URL = "https://www.marketplace.org/feed/podcast/marketplace/"
EPISODE_FOLDER = "episodes"
FRAME_RATE = 16000

@dag(
    dag_id='podcast_summary',
    schedule_interval="@daily",
    start_date=pendulum.datetime(2022, 5, 30),
    catchup=False,
)
def podcast():
    create_database = SqliteOperator(
        task_id='create_table',
        sql=r"""
        CREATE TABLE IF NOT EXISTS episodes (
            link TEXT PRIMARY KEY,
            title TEXT,
            filename TEXT,
            published TEXT,
            description TEXT,
            transcript TEXT
        );
        """,
        sqlite_conn_id="podcasts"
    )

    @task()
    def Get_Episodes():
        data = requests.get(PODCAST_URL)
        feed = xmltodict.parse(data.text)
        episodes = feed["rss"]["channel"]["item"]
        print(f"Found {len(episodes)} episodes.")
        return episodes

    podcast_episodes = Get_Episodes()
    create_database.set_downstream(podcast_episodes)

    @task()
    def load(episodes):
        hook = SqliteHook(sqlite_conn_id="podcasts")
        stored_episodes = hook.get_pandas_df("SELECT * from episodes;")
        new_episodes = []
        for episode in episodes:
            if episode["link"] not in stored_episodes["link"].values:
                filename = f"{episode['link'].split('/')[-1]}.mp3"
                new_episodes.append([episode["link"], episode["title"], episode["pubDate"], episode["description"], filename])

        hook.insert_rows(table='episodes', rows=new_episodes, target_fields=["link", "title", "published", "description", "filename"])
        return new_episodes

    new_episodes = load(podcast_episodes)

    @task()
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

        return audio_files

    audio_files = download(podcast_episodes)

  

summary = podcast()