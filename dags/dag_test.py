from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator  # Atualizado para a versão mais recente

# Definindo o DAG
with DAG(
        'dag_test',
        start_date=days_ago(2),
        schedule_interval='@daily'
) as dag:

    # Definindo as tarefas
    tarefa_1 = EmptyOperator(task_id='tarefa_1')
    tarefa_2 = EmptyOperator(task_id='tarefa_2')
    tarefa_3 = EmptyOperator(task_id='tarefa_3')
    tarefa_4 = BashOperator(
        task_id='create_folder',
        bash_command='mkdir -p "/root/Documentos/pipeline-airflow/dags_folders/folder={{data_interval_end}}"'
    )

    # Definindo a ordem das tarefas
    tarefa_1 >> [tarefa_2, tarefa_3]
    tarefa_3 >> tarefa_4
