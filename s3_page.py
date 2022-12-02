import os
import streamlit as st
import boto3
import csv
import pandas as pd
import s3fs
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

client = boto3.client("s3")
s3 = boto3.resource("s3")

response = client.list_buckets()

bucket_list = response['Buckets']
bucket = st.selectbox("Select the bucket", (f"{el['Name']}" for el in bucket_list))
my_bucket = s3.Bucket(bucket)

files_list = ["None"]
for obj in my_bucket.objects.all():
    files_list.append(obj.key)

file_selected = st.selectbox("Select the file", (f"{bucket_object}" for bucket_object in files_list))

if file_selected is not "None":
    bucket_file = None
    for bucket_object in my_bucket.objects.all():
        if bucket_object.key == file_selected:
            bucket_file = bucket_object
            break
    if bucket_file is not None:
        df = pd.read_csv("s3://{}/{}".format(bucket, bucket_file.key))
        st.write(df)

        st.download_button(
            label="Download file ⬇️",
            data=df.to_csv().encode('utf-8'),
            file_name=bucket_file.key,
            mime='text/csv',
        )

        if st.button("Delete file ❌"):
            client.delete_object(Bucket=bucket, Key=bucket_file.key)


uploaded_file = st.file_uploader("Choose a file", type={"csv", "txt", "json", "hdf"})
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.to_csv("s3://{}/{}".format(bucket, uploaded_file.name), index=False)
    st.warning('{} was uploaded successfully!'.format(uploaded_file.name))
