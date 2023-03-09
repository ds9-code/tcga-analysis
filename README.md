## Introduction - Data Download Procedure

The Genomic Data Commons (GDC) portal offers API access to download clinical, image and genomic data for patient cases.
We will leverage Python to access the API endpoints and download case data related to TCGA.

### Search Data

We can query the GDC API using a wide set of parameters to return results of a search or details about a specific entity.
The API provides helper features to assist the user in building their query and understand available fields.

### Download Files

The GDC API can be used to serve data to the user. 
If restricted data is requested, a token must be provided by the user along with the API call. 
This token can be downloaded directly from the GDC Data Portal or the GDC Data Submission Portal.


### Data Download Process

**1. TCGA case data extraction** - Identify relevant fields from the data model.
Here we choose all patients under the TCGA program.

* Create variable for the cases API endpoint

```cases_endpt = "https://api.gdc.cancer.gov/cases"```

* Create a dictionary for the fields we want to retrieve

```fields = [
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
```
* Apply the filter to extract records related to the TCGA program 

```
filters = {
            "op": "in",
            "content":{
            "field": "project.program.name",
            "value": ["TCGA"]
            }
    }
```

* Convert the filters parameter from a dictionary to JSON-formatted string and use a POST request to get the data

```
params = {
    "filters": json.dumps(filters),
    "fields": fields,
    "format": "JSON",
    "size": "11500"
    }

response = requests.post(cases_endpt, headers = {"Content-Type": "application/json"}, json = params)
```

### Important links

* GDC API - https://gdc.cancer.gov/developers/gdc-application-programming-interface-api
* GDC API User Guide - https://docs.gdc.cancer.gov/API/Users_Guide/Getting_Started/
* GDC Portal Authentication Token - https://docs.gdc.cancer.gov/Data_Portal/Users_Guide/Cart/#gdc-authentication-tokens
