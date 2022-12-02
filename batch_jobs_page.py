import os
import streamlit as st
import boto3


def list_jobs_by_status(job_definition, job_queue):
    """
    Returns a dictionary of all jobs, grouped by their status.
    Example:
    {
        "RUNNING": [ job1…, job2… ],
        "PENDING": [ job3…, job4… ],
    }
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.list_jobs
    """
    client = boto3.client("batch")
    paginator = client.get_paginator("list_jobs")

    response_iterator = paginator.paginate(
        jobQueue=job_queue,
        filters=[{"name": "JOB_DEFINITION", "values": [job_definition]}],
    )

    jobs = {}  # 'status' => [jobs…]
    for page in response_iterator:
        for job in page["jobSummaryList"]:
            jobs.setdefault(job["status"], []).append(job)

    return jobs


def list_job_definitions():
    client = boto3.client("batch")
    job_definitions = client.describe_job_definitions()
    return job_definitions['jobDefinitions']


def list_job_queues():
    client = boto3.client("batch")
    job_queues = client.describe_job_queues()
    return job_queues["jobQueues"]


def unique(list1):
    unique_list = []

    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


job_queue = st.selectbox("Select the job queue", (f"{el['jobQueueName']}" for el in list_job_queues()))

all_job_definitions = list_job_definitions()

all_jd_names = []
for el in all_job_definitions:
    all_jd_names.append(el['jobDefinitionName'])
    print("jb definition---" + str(el) + "\n")

print(all_jd_names)
all_jd_names = unique(all_jd_names)
print(all_jd_names)

job_df = st.selectbox("Select the job definition", (f"{el}" for el in all_jd_names))

form = st.form(key='submit-form')
job_name = form.text_input('Enter the batch job name here:')
submit = form.form_submit_button('Submit')

my_jd_arn = None

for el in all_job_definitions:
    if el['jobDefinitionName'] == job_df:
        my_jd_arn = el['jobDefinitionArn']

my_jq_arn = None
all_job_queues = list_job_queues()
for el in all_job_queues:
    if el['jobQueueName'] == job_queue:
        my_jq_arn = el['jobQueueName']

if submit:
    client = boto3.client("batch")
    response = client.submit_job(
        jobName=job_name,
        jobDefinition=my_jd_arn,
        jobQueue=my_jq_arn,
        propagateTags=True
    )
    job_id = response["jobId"]
    st.success(f"Job '{job_id}' submitted successfully. ✅")

job_status = st.selectbox("Select status",
                          ('SUBMITTED', 'PENDING', 'RUNNABLE', 'STARTING', 'RUNNING', 'SUCCEEDED', 'FAILED'))

lista = list_jobs_by_status(my_jd_arn, my_jq_arn)
job_list = []
flag = False
for key in lista.keys():
    if job_status == key:
        for el in lista[job_status]:
            job_list.append(el)
            flag = True

if not flag:
    st.warning("There aren't any jobs with this selected status!")
else:
    new_job_list = []
    for el in job_list:
        new_job_list.append(el)
    job = st.selectbox("These are the jobs with the selected status:", (f"{el['jobName']}" for el in new_job_list))
