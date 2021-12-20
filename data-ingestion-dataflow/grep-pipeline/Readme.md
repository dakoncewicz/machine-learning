Lab : Dataflow simple pipeline
This Lab demonstrates how to write simple dataflow job using Python. This job countes how many times occours one particular word in source files. In this case we will search "import" word in *.java files (./java catalog).
This lab is part of https://codelabs.developers.google.com/codelabs/cpb101-simple-dataflow-py 

Lab is splited into two phases :
- demonstrates how to run sample Python programm on local machine using Apache Beam python library
- next how to run cloud version of this programm into Google Cloud environemnt
- you can compare this two version of the same functionality ran on your local machine and in cloud environment - both using Apache Beam.
#### Step 1 Run set up package with Admin privilages
- clone the  repo https://github.com/dakoncewicz/machine-learning/dataflow-simple-pipeline  to your local machine 
- from the Cloud Shell, change the current catalog to ./machine-learning/dataflow-simple-pipeline
- run bash script `install_packages.sh` with administration privilages
```
$ sudo ./install_packages.sh
```
- check the version of instaled pip is correct
```
$ pip -V
```

#### Step 2 Run the grep_pipeline_local.py program on your local machine
- on your local machine run the `grep_pipeline_local.py` program in Cloud Shell
```
$ python grep_pipeline_local.py
```
- this is the local execution not in the cloud. 
- Note: if you found the warning after execution programm just ignore it; this warning just means that logs will be written to stderr
- check te output of the program
```
$ cat /tmp/grep_pipeline_ouyput-*
```

#### Step 3 Run the grep_pipeline_cloud.py using Dataflow
- on your left side navigation bar go to Dataflow 
- Note : while using Dataflow in a Cloud we cannot get the file from a local machine, we need to copy this sample java files onto GCP
- run the command
```
$ gsutil cp ./java/*.java gs://mlbq-my-bucket/java
```
- enable Dataflow API 
  - from leftside navigation bar select the API Manager > Dashboard and run it
  - click the button [Enable API] on the top
  - search the Dataflow 
- within the programm `grep_pipeline_cloud.py` check the variables: PROJECT_ID, BUCKET _ID and BUCKET_FOLDER
- run the cloud version of grep_pipeline programm
```
$ python grep_pipeline_cloud.py
```

#### Step 4 Check your Lab succesed 
- go to the Cloud Console and in the Dataflow service find the job `goodjob`, click on it
- on the right side bar menu you can find the basic metrics of the Dataflow job
#### Step 5 Clean your resources
To avoid incurring charges to your Google Cloud account for the resources used on this page, follow these steps.

Note: If you followed this quickstart in a new project, then you can delete the project.
In the Cloud Console, go to the Cloud Storage Browser page.
[`Go to Browser`]

Click the checkbox for the bucket that you want to delete.
To delete the bucket, click [`Delete`] button, and then follow the instructions.