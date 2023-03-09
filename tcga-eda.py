# -*- coding: utf-8 -*-
"""tcga-joint-representation-data.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
pd.set_option('display.max_colwidth', None)

#Direct URL
#tcga_url = 'https://api.gdc.cancer.gov/cases?filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.program.name%22%2C%22value%22%3A%5B%22TCGA%22%5D%7D%7D%5D%7D'

import requests
import json

fields = [
    "case_id",
    "submitter_id",
    "project.program.name",
    "project.project_id",
    "demographic.ethnicity",
    "demographic.gender",
    "demographic.race",
    "primary_diagnosis",
    "diagnoses.icd_10_code",
    "diagnoses.age_at_diagnosis",
    "disease_type",
    "primary_site",
    "demographic.year_of_birth",
    "demographic.year_of_death",
    "demographic.days_to_death",
    "demographic.vital_status"
    ]

fields = ",".join(fields)

cases_endpt = "https://api.gdc.cancer.gov/cases"

filters = {
            "op": "in",
            "content":{
            "field": "project.program.name",
            "value": ["TCGA"]
            }
    }

# With a GET request, the filters parameter needs to be converted
# from a dictionary to JSON-formatted string

params = {
    "filters": json.dumps(filters),
    "fields": fields,
    "format": "JSON",
    "size": "11500"
    }

response = requests.post(cases_endpt, headers = {"Content-Type": "application/json"}, json = params)
#print(response.content.decode("utf-8"))

data = json.loads(response.content.decode('utf-8'))

df = pd.json_normalize(data['data'], 'hits')

df.head()

#Summary Statistics of numeric and categorical features
df.describe(include='all')

df.isna().sum()/df.shape[0]

# Missing value check by feature
df.isnull().sum()

df.groupby('disease_type').disease_type.count().plot(kind='bar', figsize=(16,9))
plt.show()

df.groupby('primary_site').disease_type.count().plot(kind='bar', figsize=(16,9))
plt.show()

plt.subplot(221)
df['demographic.gender'].value_counts().plot(kind='bar', title='Gender', figsize=(16,9))
plt.xticks(rotation=0)

plt.subplot(222)
df['demographic.ethnicity'].value_counts().plot(kind='bar', title='Ethinicity')
plt.xticks(rotation=0)

plt.subplot(223)
df['demographic.vital_status'].value_counts().plot(kind='bar', title='Vital Status')
plt.xticks(rotation=0)


plt.show()

sns.displot(df['demographic.days_to_death'])

#corr = df.corr()
#sns.heatmap(corr, annot=True, square=True)
#plt.yticks(rotation=0)
#plt.show()

df_ov = pd.pivot_table(
    data=df,
    values='demographic.days_to_death', 
    index='disease', 
    columns=None, 
    aggfunc='mean', 
    fill_value=None, 
    margins=False, 
    dropna=True, 
    margins_name='All', 
    observed=False,
    sort=True
)