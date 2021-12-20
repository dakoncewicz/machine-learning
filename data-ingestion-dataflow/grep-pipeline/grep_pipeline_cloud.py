#!/usr/bin/env python


import apache_beam as beam
import re

def custom_grep(line, search_query):

   if re.match( r'^' + re.escape(search_query), line):

      yield line

PROJECT_ID = 'udemy-data-engineer-210920'
BUCKET_ID = 'udemy-data-engineer-210920'
BUCKET_FOLDER = 'dataflow-pipeline-py'


def run():

   argv = [
      '--project={0}'.format(PROJECT_ID),
      '--job_name=goodjob',
      '--save_main_session',
      '--staging_location=gs://{0}/{1}/staging/'.format(BUCKET_ID, BUCKET_FOLDER),
      '--temp_location=gs://{0}/{1}/staging/'.format(BUCKET_ID, BUCKET_FOLDER),
      '--runner=DataflowRunner'
   ]

   pipeline = beam.Pipeline(argv=argv)

   input = 'gs://{0}/{1}/input/*.java'.format(BUCKET_ID, BUCKET_FOLDER)

   output_prefix = 'gs://{0}/{1}/output'.format(BUCKET_ID, BUCKET_FOLDER)

   search_query = 'import'

   # find all lines that contain the searchTerm
   (pipeline
      | 'GetInput' >> beam.io.ReadFromText(input)
      | 'Grep' >> beam.FlatMap(lambda line: custom_grep(line, search_query) )
      | 'WriteOutput' >> beam.io.WriteToText(output_prefix)
   )

   pipeline.run()

if __name__ == '__main__':

   run()
