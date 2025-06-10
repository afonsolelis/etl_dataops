import os
import pandas as pd
import streamlit as st
from clickhouse_driver import Client

CLICKHOUSE_HOST = os.environ.get('CLICKHOUSE_HOST', 'clickhouse')
CLICKHOUSE_PORT = int(os.environ.get('CLICKHOUSE_PORT', '9000'))
CLICKHOUSE_USER = os.environ.get('CLICKHOUSE_USER', 'default')
CLICKHOUSE_PASSWORD = os.environ.get('CLICKHOUSE_PASSWORD', '')
CLICKHOUSE_DB = os.environ.get('CLICKHOUSE_DB', 'default')
TABLE_NAME = 'ingestions'

client = Client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, user=CLICKHOUSE_USER, password=CLICKHOUSE_PASSWORD)

def load_data():
    query = f"SELECT id, ingestion_date, data_value FROM {TABLE_NAME} ORDER BY id"
    data = client.execute(query)
    df = pd.DataFrame(data, columns=['id', 'ingestion_date', 'data_value'])
    return df

def main():
    st.title('DataOps ETL Dashboard')
    df = load_data()
    st.metric('Total Rows', len(df))
    if not df.empty:
        last_ingestion = df['ingestion_date'].max()
        st.metric('Last Ingestion', last_ingestion)
    st.dataframe(df)

if __name__ == '__main__':
    main()
