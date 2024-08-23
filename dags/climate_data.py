#Importing Libraries
from airflow import DAG
import pendulum
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.macros import ds_add
from os.path import join
import pandas as pd

#Creating DAG instance
with DAG(
        "climate_data",
        start_date=pendulum.datetime(2024, 7, 29, tz="UTC"),
        schedule_interval='0 0 * * 1', # executar toda segunda feira
    ) as dag:

    #
    task_1 = BashOperator(
        task_id = 'create_folder',
        bash_command = 'mkdir -p "/root/Documentos/pipeline-airflow/generated_documents/semana={{data_interval_end.strftime("%Y-%m-%d")}}"'
    )

    def extract_data(data_interval_end):
        
        city = 'Boston'
        key = 'GNUN6LMMFTZLAESBYXKCZK56M'

        URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
        f'{city}/{data_interval_end}/{ds_add(data_interval_end, 7)}?unitGroup=metric&include=days&key={key}&contentType=csv')

        data = pd.read_csv(URL)

        file_path = f'/root/Documentos/pipeline-airflow/generated_documents/semana={data_interval_end}/'

        data.to_csv(file_path + 'dados_brutos.csv')
        data[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temperaturas.csv')
        data[['datetime', 'description', 'icon']].to_csv(file_path + 'condicoes.csv')

    task_2 = PythonOperator(
        task_id = 'extract_data',
        python_callable = extract_data,
        op_kwargs = {'data_interval_end': '{{data_interval_end.strftime("%Y-%m-%d")}}'}
    )

    task_1 >> task_2