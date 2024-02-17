from google.cloud import bigquery
import os
import pandas as pd
from sklearn.cluster import KMeans


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/phunghongquan/Documents/semester5/DataWarehouse/demo1/dags/quan-test-project.json'
def train_model():
    client = bigquery.Client()

    # Construct a reference to the table
    table_ref = client.dataset('OLAP').table('Fact_Table')

    # Execute a SQL query
    query = f"SELECT CustomerID, MAX(Recency) AS Recency, MAX(Frequency) AS Frequency FROM `OLAP.Fact_Table` GROUP BY CustomerID;"
    
    query_job = client.query(query)

    df = query_job.to_dataframe()

    df['Recency'].fillna(df['Recency'].median(), inplace=True)

    # Extract the 'CustomerID' column
    customer_ids = df['CustomerID']

    # Create a KMeans model using only 'Recency' and 'Frequency'
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(df[['Recency', 'Frequency']])

    # Get the cluster labels
    labels = kmeans.labels_

    # Create a DataFrame with 'CustomerID', 'Recency', 'Frequency', and 'label'
    df_with_labels = pd.DataFrame({'CustomerID': customer_ids, 'Recency': df['Recency'], 'Frequency': df['Frequency'], 'label': labels})

    # Push the clustered data to BigQuery
    clustered_table_ref = client.dataset('OLAP').table('Clustered_Customers')
    job = client.load_table_from_dataframe(df_with_labels, clustered_table_ref)  # Make an API request.

    return True
