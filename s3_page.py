import os
import streamlit as st
import boto3
import csv
import pandas as pd
import s3fs
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

client = boto3.client("s3")
s3 = boto3.resource("s3")
# s3 = boto3.resource('s3')
# bucket = s3.Bucket('merx-test-bucket')

response = client.list_buckets()
# Output the bucket names
# for bucket in response['Buckets']:
# print(f'  {bucket["Name"]}')

bucket_list = response['Buckets']
bucket = st.selectbox("Select the bucket", (f"{el['Name']}" for el in bucket_list))
my_bucket = s3.Bucket(bucket)

#if bucket:
#    file = st.selectbox("Select the file", (f"{str(el.key)}" for el in my_bucket.objects.all()))

    #c1, c2, c3 = st.columns(3)

    #with c1:
#    if st.button("Open file 📖"):
#        df = pd.read_csv("s3://{}/{}".format(bucket, file))
#        st.write(df)
    #with c2:
#    df = pd.read_csv("s3://{}/{}".format(bucket, file))
#    st.download_button(
#            label="Download file ⬇️",
#            data=df.to_csv().encode('utf-8'),
#            file_name=file,
#            mime='text/csv',
#        )
    #with c3:
#    if st.button("Delete file ❌"):
#        print("key---" + str(file.key))
#        print("bucket name ----" + str(bucket))
            # s3.Object(my_bucket, bucket_object.key).delete()
#        client.delete_object(Bucket=bucket, Key=file.key)
            # print("object deleted!" + str(resp))

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
            print("key---" + str(bucket_file.key))
            print("bucket name ----" + str(bucket))
            # s3.Object(my_bucket, bucket_object.key).delete()
            client.delete_object(Bucket=bucket, Key=bucket_file.key)
            # print("object deleted!" + str(resp))

#for bucket_object in my_bucket.objects.all():
#     if st.button(bucket_object.key):
#         #print("object key" + str(bucket_object.key))
#         #print("bucket"+str(bucket))
#         df = pd.read_csv("s3://{}/{}".format(bucket, bucket_object.key))
#         st.write(df)
#         # AgGrid(df)
#         # print(df)
#         c1, c2, c3, c4 = st.columns(4)
#         with c2:
#             if st.button("test button"):
#                 print("testing button")
#         with c3:
#             print("Downloading file---")
#             st.download_button(
#                 label="Download file ⬇️",
#                 data=df.to_csv().encode('utf-8'),
#                 file_name=bucket_object.key,
#                 mime='text/csv',
#             )
#
#         with c4:
#             if st.button("Delete file ❌"):
#                 print("key---" + str(bucket_object.key))
#                 print("bucket name ----" + str(bucket))
#                 #s3.Object(my_bucket, bucket_object.key).delete()
#                 client.delete_object(Bucket=bucket, Key=bucket_object.key)
#                # print("object deleted!" + str(resp))
#     else:
#         continue
#     # body = bucket_object.get()['Body'].read()
#     # st.write(body)

uploaded_file = st.file_uploader("Choose a file", type={"csv", "txt", "json", "hdf"})
if uploaded_file:
    # client.upload_file(uploaded_file.name, bucket, uploaded_file.name)
    # print(uploaded_file.name)
    df = pd.read_csv(uploaded_file)
    df.to_csv("s3://{}/{}".format(bucket, uploaded_file.name), index=False)
    st.warning('{} was uploaded successfully!'.format(uploaded_file.name))
# for my_bucket_object in response.objects.all():


# for my_bucket_object in response.objects.all():

#    print(my_bucket_object)

# fs = s3fs.S3FileSystem(anon=False)

#    print(my_bucket_object)

# fs = s3fs.S3FileSystem(anon=False)

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
# @st.experimental_memo(ttl=600)
# def read_file(filename):
#    with fs.open(filename) as f:
#        return f.read().decode("utf-8")

# content = read_file("merx-test-bucket/kaggle_train_nesp.csv")

# st.write(content)
# Print results.
# for line in content.strip().split("\n"):
#    name, pet = line.split(",")
#    st.write(f"{name} has a :{pet}:")
