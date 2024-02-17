from google.cloud import bigquery
import airflow
from airflow.models.dag import DAG
from datetime import timedelta, datetime
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.contrib.operators.bigquery_to_gcs import BigQueryToCloudStorageOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from clustering import train_model
from google.cloud import storage
import os
import pandas as pd


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/opt/airflow/data/demo1/dags/quan-test-project.json'

default_args = {
    'owner': 'phungquan',
    # 'start_date': airflow.utils.dates.days_ago(0), # chưa hiểu function này
    'start_date': None, # YYYY-MM-DD
    'retries': None,
    'retry_daylsy': None
}

dag = DAG(
    'OLTP_to_OLAP',
    # template_searchpath=["/opt/airflow/data/demo1/dags"],
    default_args=default_args,
    description='Run BigQuery SQL query',
    schedule_interval=None,
)

#------------Query-------------#

def read_sql_file(file_path):
  with open(file_path, 'r') as file:
    return file.read()

#------------Read Query-------------#
DimCustomer_sql_query = read_sql_file('/opt/airflow/dags/SQL_query/dim_customer.sql')
DimDate_sql_query = read_sql_file('/opt/airflow/dags/SQL_query/dim_date.sql')
DimProduct_sql_query = read_sql_file('/opt/airflow/dags/SQL_query/dim_products.sql')
DimOrderDetails_sql_query = read_sql_file('/opt/airflow/dags/SQL_query/dim_order_details.sql')
FactOrderTemp_sql_query = read_sql_file('/opt/airflow/dags/SQL_query/fact_table_temp.sql')
RFM_Agg_sql_query = read_sql_file('/opt/airflow/dags/SQL_query/rfm_agg.sql')
Product_Agg_sql_query = read_sql_file('/opt/airflow/dags/SQL_query/product_agg.sql')
FactOrder_sql_query = read_sql_file('/opt/airflow/dags/SQL_query/fact_table.sql')



# DimTable_sql = '/opt/airflow/data/demo1/dags/create-update-DimProduct.sql'
t1 = BigQueryOperator(
    task_id='create_update_dim_customer',
    sql= DimCustomer_sql_query,
    use_legacy_sql=False,  
    write_disposition='WRITE_TRUNCATE',
    create_disposition='CREATE_IF_NEEDED',  
    dag=dag,
)

t2 = BigQueryOperator(
    task_id='create_update_dim_date',
    sql= DimDate_sql_query,
    use_legacy_sql=False,  
    write_disposition='WRITE_TRUNCATE',
    create_disposition='CREATE_IF_NEEDED',  
    dag=dag,
)

t3 = BigQueryOperator(
    task_id='create_update_dim_product',
    sql= DimProduct_sql_query,
    use_legacy_sql=False,  
    write_disposition='WRITE_TRUNCATE',
    create_disposition='CREATE_IF_NEEDED',  
    dag=dag,
)

t4 = BigQueryOperator(
    task_id='create_update_dim_order_details',
    sql= DimOrderDetails_sql_query,
    use_legacy_sql=False,  
    write_disposition='WRITE_TRUNCATE',
    create_disposition='CREATE_IF_NEEDED',  
    dag=dag,
)

t5 = BigQueryOperator(
    task_id='create_update_fact_table_temp',
    sql= FactOrderTemp_sql_query,
    use_legacy_sql=False,  
    write_disposition='WRITE_TRUNCATE',
    create_disposition='CREATE_IF_NEEDED',  
    dag=dag,
)

t6 = BigQueryOperator(
    task_id='create_update_rfm_agg',
    sql= RFM_Agg_sql_query,
    use_legacy_sql=False,  
    write_disposition='WRITE_TRUNCATE',
    create_disposition='CREATE_IF_NEEDED',  
    dag=dag,
)

t7 = BigQueryOperator(
    task_id='create_update_product_agg',
    sql= Product_Agg_sql_query,
    use_legacy_sql=False,  
    write_disposition='WRITE_TRUNCATE',
    create_disposition='CREATE_IF_NEEDED',  
    dag=dag,
)

t8 = BigQueryOperator(
    task_id='create_update_fact_table',
    sql= FactOrder_sql_query,
    use_legacy_sql=False,  
    write_disposition='WRITE_TRUNCATE',
    create_disposition='CREATE_IF_NEEDED',  
    dag=dag,
)

def model_training():
   train_model()

t9 = PythonOperator(
    task_id='train_model',
    python_callable=model_training,
    dag=dag
)

TaskDelay = BashOperator(task_id="delay_bash_task",
                         dag=dag,
                         bash_command="sleep 5s")

bq_to_gcs_task = BigQueryToCloudStorageOperator(
    task_id='bigquery_to_gcs_task',
    source_project_dataset_table='northwind-qu.OLAP.Fact_Table',  # Replace with your BigQuery table
    destination_cloud_storage_uris=['gs://fact-table-storage/fact_table.avro'],  # Replace with your GCS bucket and file
    compression='NONE',  # Compression type: 'NONE', 'GZIP', etc.
    export_format='AVRO',  # Export format: 'CSV', 'NEWLINE_DELIMITED_JSON', etc.
    field_delimiter=',',  # Field delimiter for CSV format
    print_header=True,  # Print header in CSV file
    dag=dag
)

[t1, t2, t3, t4] >> TaskDelay>> t5 >> [t6, t7] >> t8 >> t9 >> bq_to_gcs_task

# t1 >> t2 >> TaskDelay >> t3
# t3 >> t5
# [t1, t2] >> t4

if __name__ == "__main__":
    dag.cli()







