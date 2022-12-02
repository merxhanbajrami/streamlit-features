import os
import streamlit as st
import boto3
import csv
import pandas as pd
import s3fs
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import psycopg2

client = boto3.client('rds')
databases = client.describe_db_instances()
# st.write(databases)

databases_list = ["None"]
for el in databases["DBInstances"]:
    databases_list.append(el['DBInstanceIdentifier'])

database_selected = bucket = st.selectbox("Select the db instance", (f"{el}" for el in databases_list))

if database_selected != "None":
    if database_selected:
        username = st.text_input('Enter username')
        password = st.text_input('Enter your password', type="password")
        if username is not "" and password is not "":
            port = ""
            host = ""
            database_engine = ""
            for db in databases["DBInstances"]:
                if db['DBInstanceIdentifier'] == database_selected:
                    host = db["Endpoint"]["Address"]
                    port = db["Endpoint"]["Port"]
                    database_engine = db["Engine"]

            # engine = psycopg2.connect(
            #    database="postgres",
            #    user="postgres",
            #    password="immuneeringv3test",
            #    host="immuneering-v3-test-postgre.cverz3y5jpp2.eu-west-1.rds.amazonaws.com",
            #    port='1889'
            # )

            engine = psycopg2.connect(
                database=database_engine,
                user=username,
                password=password,
                host=host,
                port=port
            )


            cursor = engine.cursor()

            cursor.execute("""SELECT relname FROM pg_class WHERE relkind='r'
                              AND relname !~ '^(pg_|sql_)';""") # "rel" is short for relation.

            tables = [i[0] for i in cursor.fetchall()] # A list() of tables.
            table = st.selectbox("Select the table name",(f"{el}" for el in tables))

            sql = "select * from {};".format(table)
            data = pd.read_sql_query(sql, engine)
            st.write("Data loaded:")
            st.write(data)

            #print(engine)
            #st.write(engine)


# st.write(databases["DBInstances"])