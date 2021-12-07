# machine-learning
This Repo contains Google Cloud oriented data loading and machine learning examples and templates.
--------------------------------------------------------------
Table of contents placeholder

--------------------------------------------------------------

Comparing the Machine Learning (ML) options available in GCP :
- Cloud AutoML - for those who want to use read-to-use models and bild their own soluton on it
- BigQuery ML - allows SQL users to build ML solution based on data in BigQuery and avoid having to export data to develop models in Java or Python
- Kubeflow - supports deploying scalable pipelines in Kubernetes and contenerized worlds
- Spark MLib - is comprehensive set of math and ML tools that can be used when deploying Cloud Dataproc cluster
  
--------------------------------------------------------------
# BigQuery Machine Learning (BigQuery ML)
## 1. BigQuery overview
### 1.1 BigQuery Managed Storage Warehouse
Foundtion of BigQuery service : 
- Managed services - provisioning underlaying vm-s, patching, maintaining, backups etc is Google responsabilities
- Serverless data warehouse:
  - petabyte scale
  - uses SQL but is not a relational database :
    - Tables are stored in optymized columnar format
    - Each table is compresed and encrypted on disk
- Storage is durable and each table is replicated across datacenters
- Supports natively batch and streaming ingestion

For BigQuery detailed documentations see: https://cloud.google.com/bigquery/docs
### 1.2 BigQuery Datasets & Tables
BigQuery has a logical structure that organizaes data around struture called __Dataset__. 
- Dataset is a collection of tables and views
- Access control is set at dataset level
- Tables :
  - support scalar formats but nested and repeated structures as well
  - partitioning makes easier to  isolate the data that is usefull to respond to a particular query and it reduces amount of scanning (which is important from biling perspective).
- Views :
  - similar to traditional data bases - it is projection of one or more tables (plus agregation, filtering etc)
  - tables can be joined
  - views can be materialized
- Federated Data Access - you can access and query data that`s stored in different storage system: 
  - Cloud Storage :
    - Parquet
    - ORC
  - Bigtable (Google Cloud Bigdata storage system) and Cloud SQL
  - Spreadsheets in Google Drive
### 1.3 BigQuery Machine Learning
BigQueryML - excellent choice for persons who knows SQL, manipulation on data and have good understanding of busines problem to solve.
- Create machine learning models in SQl
- Several kinds of models:
    - Linear regression
    - Binary and multiclass logistic regressions
    - K-menas clustering
    - Time series forecast
    - Matrix factorisation
    - Bosted Tree and XGBoost
    - TensorFlow (imported)
- AutoML Tables = interesing feature for those who does not much to know about ML but rather has expertise in business domain
## 2. Data Loading Best Bracticies
### 2.1 Data loading overview
- Batch ingest is free
- Doesn`t consume query capacity (important from biling perspective)
- ACID semantics 
- Load Petabytes per day
- Possible load data sources:
  - Cloud Storage
  - Local machine
  - Streaming inserts (Streaming API for real-time) 
  - DML Bulk loads
  - BigQuery I/O Transform in Cloud Dataflow

### 2.2 Best Practices: Data format
Faster >> Slower
- __AVRO (compressed)__ - __the fastest__
  - Avro (uncompressed)
  - Parquet /ORC
  - CSV                                   
  - JSON
  - CSV (compressed)
- __JSON (compressed)__ - __the slowest__

### 2.3 Best Practicies : ELT / ETL

![best practices img](./resources/images/best-practices-etl-elt.001.png)

source : Data Warehousing With BigQuery: Best Practices (Cloud Next '19) link: https://www.youtube.com/watch?v=ZVgt1-LfWW4
## 3. Data loading examples
This chapter explains step-by-step how to ingest data into a BigQuery Data Warehouse starting from the simplest way direct batch loading.
Picture bellow explains end-to-end process in terms of Google Cloud components or services.

![end to end process img](./resources/images/end-to-end-example-001.png)

source : Data Warehousing With BigQuery: Best Practices (Cloud Next '19) link: https://www.youtube.com/watch?v=ZVgt1-LfWW4

Batch loading process can be managed in following steps:
1. Load the data source files (sometimes called feeds) into Google Cloud Storage. GCS can be viewed as Data Lake component. As a principle use: one batch = one file in GCS = one raw-data table.
2. Next load the files into BigQuery Raw Data area using Dataflow. Use simple checks to pass proper records only or augment the default parameters. This is the first step of data cleansing.
3. Transform data from Raw Data into Staging Area tables using SQL language to easily transform data, join data from multiple raw data sources, calculate some missing parameters (eg. agregation) etc.
4. Staging Area are - so called - golden source of information for reporting or machine-learning purposes.
5. Steps 4 and 5 can be split into several subtasks if needed; it can be easily managed by using Cloud Composer service.

In the next sections we see (in the Lab manner) how to load the data using several approaches:
1. Direct batch ingestion - loading data directly from the Google Cloud Storage
2. Batch loading data using a Dataflow Template (from the console)
3. Batch loading data running simple Dataflow pipeline (from the Cloud Shell)
4. Streaming loading using Dataflow + Pub/Sub queues (comming soon)
### 3.1 Lab  1: Direct batch ingestion
This scenario is based on loading files directly from Google Cloud Storage (GCS) __without__ Dataflow service. In that case GCS can be seen like a Data Lake component, which manages the archive source data (it means already loaded data) as well. GCS is cloud cheapest storage so it is optimal in terms of cost and project budget. 
Using GCS as a starting point should be common element of every batch loading solution architecture.

#### Step 1 Setup and requirements
- Signin to Cloud Console and create a new project or reuse an existing one. (If you don't already have a Gmail or G Suite account, you must create one.). Note : memorize the url : __console.cloud.google.com__.
- From the cosole, run the Cloud Shell
- Run the following command in Cloud Shell to confirm whether you are authenticated:
```
gcloud auth list
```
  - in response, you shoud see in Cloud Shell the following command output :
```
 Credentialed Accounts
ACTIVE  ACCOUNT
*       <my_account>@<my_domain.com>
```
- To set the active account, run:
```
    $ gcloud config set account `ACCOUNT`
```
- list the available projects
```
gcloud config list project
```
  - the expected outpot should looks like this
```
[core]
project = <PROJECT_ID>
```
  - if NOT, setup the project, using bellow commands
```
gcloud config set project <PROJECT_ID>
```

#### Step 2 Move data from a file system into Cloud Storage
- From: https://github.com/dakoncewicz/machine-learning/resources/source-files/babynames download names.zip file. Then unpack this file on your local machine.
- In the Cloud Shell, first create `ml-my-bucket` bucket in `us-east1` location than load sample files from local drive.
```
$ gsutil mb  -c standard -l us-east1 gs://mlbq-my-bucket
$ gsutil mv ./dir gs://mlbq-my-bucket
```
#### Step 3 Load data from GCS to BigQuery
- In the Cloud Shell run the following command
```
 bq load —source_format=CSV \ 
> gs://mlbq-my-bucket/babynames/*.txt \
> name:string,gender:string,count:integer 
```
- __Note:__
  - --source_format=CSV - specify the load file format
  - line 'name:string,gender:string,count:integer' specifies the schema
- be aware of some limitations when using bq load command
  - CSV files do not support nested or repeated data.
  - Remove byte order mark (BOM) characters. They might cause unexpected issues.
  - If you use gzip compression, BigQuery cannot read the data in parallel. Loading compressed CSV data into BigQuery is slower than loading uncompressed data.
  - other limitations see: https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv#limitations
  
#### Step 4 Verify whether data is loaded correctly
- in the Cloud Shell run the query
```
$ bq query “SELECT name, count FROM babynames.all_names WHERE gender = 'F’ ORDER BY count DESC LIMIT 5"
```
- OR you can export loaded data from BigQuery as well
```
$ bq export <tablename> gs://<bucket name> / <filename.csf>
```

#### Summary
This Lab demonstrates how to simply load text files into BigQuery table. 

### 3.2 Lab 2: Dataflow template
#### Dataflow quick overview
Dataflow is a managed service for executing a wide variety of data processing patterns. Dataflow is based on Apache Beam project.

The Apache Beam is an open source programming model that enables you to develop both batch and streaming pipelines. You create your pipelines with an Apache Beam program and then run them on the Dataflow service. The Apache Beam documentation (ref: https://beam.apache.org/documentation/ ) provides in-depth conceptual information and reference material for the Apache Beam programming model, SDKs, and other runners.

Dataflow cloud service key features:
- Enables batch and streaming processing data pipeline,
- Simplify operations and management - allows teams to focus on programming (Python, Java and Go) instead of managing server clusters
  - Dataflow's serverless approach removes operational overhead from data engineering workloads,
- Automated resource management and dynamic work rebalancing
- Flexible resource scheduling pricing for batch processing

This Lab provides a few steps to implement and run simple dataflow job transforming input file and counting how many times aeach word occours in text input files. Lab demonstrates how to use in Google Console predfined Dataflow templates. 
Next Lab will explain how to write simple dataflow job using Python.

#### Step 1 Create dataflow job from the template
- open the Console and navigate to the Dataflow panel
- go to the Dataflow >> Jobs >> Create job from a template
  
![create job from a template](./resources/images/create-dataflow-job-001.png)

- on the screen define new job, setting up the bellow parameters:
  - Job name: __dfl-job-lab2__
  - Dataflow temlplate: __wordcount__
  - Input file(s) in Cloud Storage: __gs://dataflow-samples/shakespeare/kinglear.txt__
  - Output Cloud Storage file prefix: __gs://mlbq-my-bucket/counts__
  - Teporary location: __gs://mlbq-my-bucket/temp__
  - Encryption: leave the option __Google-managed key__

#### Step 2 Run the Job
- Click the button __RUN JOB__
- Within a few seconds you will see the Job Graph, like is shown on bellow picture.

![job running graph](./resources/images/job-running-graph-001.png)

#### Step 3 Check the result
- Got o the Cloud Storage __mlbq-my-bucket__ and open one of __counts-00000n-of-00003__ files

- files contain the partly results of counting the words in public input text file __kinglear.txt__
#### Summary
This Lab demonstrates how to use Dataflow predefined template to run simple Dataflow job. Job that we have ran simply counts how many times each word appears in input file. The main ideas are:
- we can use some of templates to transform source data into data sink; in that case both are text files but we can easily transform source data into eg. BigQuery table.
- using Dataflow we can not only load the data from one place to another but make some transformations as well. 

### 3.3 Lab : Dataflow simple pipeline
This Lab demonstrates how to write simple dataflow job using Python. This job countes how many times occours one particular word in source files. In this case we will search "import" word in *.java files (./java catalog).
Lab is splited into two fases :
- demonstrates how to run sample Python programm on local machine using Apache Beam python library
- next how to move this programm into Google Cloud environemnt
#### Step 1 Run set up package with Admin privilages
- run bash script 
```
```

#### Step 1 Setup and requirements
- Sign in to Cloud Console and create a new project or reuse an existing one. (If you don't already have a Gmail or G Suite account, you must create one.). Note : memorize the url console.cloud.google.com.
- 
```
#### Step 2  Run the Cloud Shell
- From the Cloud Console, click Activate Cloud Shell 
- Run the following command in Cloud Shell to confirm that you are authenticated:
```
gcloud auth list
```
  - in response, you shoud see in Cloud Shell the following command output :
```
 Credentialed Accounts
ACTIVE  ACCOUNT
*       <my_account>@<my_domain.com>

To set the active account, run:
    $ gcloud config set account `ACCOUNT`
```
- list the available project list
```
gcloud config list project
```
  - the expected outpot should looks like this
```
  [core]
project = <PROJECT_ID>
```
  - if NOT, setup the project, using bellow commands
```
gcloud config set project <PROJECT_ID>
```

#### Step 3  Create a new Cloud Storage bucket
- 

#### Step 4 Create a Maven project
- After Cloud Shell launches, let's get started by creating a Maven project using the Java SDK for Apache Beam.
- Run the __mvn archetype:generate__ command in your shell as follows:
```
mvn archetype:generate \
     -DarchetypeGroupId=org.apache.beam \
     -DarchetypeArtifactId=beam-sdks-java-maven-archetypes-examples \
     -DarchetypeVersion=2.22.0 \
     -DgroupId=org.example \
     -DartifactId=first-dataflow \
     -Dversion="0.1" \
     -Dpackage=org.apache.beam.examples \
     -DinteractiveMode=false
```
- After running the command, you should see a new directory called first-dataflow under your current directory. first-dataflow contains a Maven project that includes the Cloud Dataflow SDK for Java and example pipelines.
#### Step 5 Run a text processing pipeline using DataFlow
#### Step 6 Check your Lab succesed 
#### Step 7 Clean your resources

### 3.4 Lab : Dataflow streaming ingestion using Pub/Sub Google Cloud queueing system (comming soon)