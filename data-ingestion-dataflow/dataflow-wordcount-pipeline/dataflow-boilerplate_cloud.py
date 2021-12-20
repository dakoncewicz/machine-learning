##################################################################################
# This is the Bolierplate code which helps you to run local Python dataflow code
# in Google Cloud as Dataflow pipeline
#
##################################################################################

import apache_beam as beam
import argparse
import re

# define constants
PROJECT_ID = 'my-dataflow-project-dk'
BUCKET_ID = 'dataflow-211220'
BUCKET_FOLDER = 'dataflow-pipeline-py'


#################################################################################
# put here your local function for searching, mapping, joining etc
# sample function custom_grep
def custom_grep(line, search_query):
    if re.match(r'^' + re.escape(search_query), line):
        yield line


#################################################################################

# pipeline Dataflow body
def run():

    # defining of cloud Dataflow job
    argv = [
        '--project={0}'.format(PROJECT_ID),
        '--job_name=goodjob',
        '--save_main_session',
        '--staging_location=gs://{0}/{1}/staging/'.format(
            BUCKET_ID, BUCKET_FOLDER),
        '--temp_location=gs://{0}/{1}/staging/'.format(
            BUCKET_ID, BUCKET_FOLDER),
        '--runner=DataflowRunner'
    ]

    # reading the input and output parameters from commandline
    parser = argparse.ArgumentParser()

    parser.add_argument('--input',
                        dest='input',
                        required=True,
                        help='Input file to process.')
    parser.add_argument('--output',
                        dest='output',
                        required=True,
                        help='Output file to write results to.')

    path_args, pipeline_args = parser.parse_known_args()

    # set up the local variables according to cmd params
    inputs_pattern = path_args.input
    outputs_prefix = path_args.output

    # creating and giving pipeline a name
    pipeline = beam.Pipeline(argv=argv)

    search_query = 'import'

    # example of pipeline - find all lines that contain the searchTerm
    # put your pipeline transformation instead of 'Grep' line

    attendance_count = (pipeline
                        | 'GetInput' >> beam.io.ReadFromText(inputs_pattern)
                        | 'Grep' >> beam.FlatMap(lambda line: custom_grep(line, search_query))
                        | 'WriteOutput' >> beam.io.WriteToText(outputs_prefix)
                        )

    # run dataflow pipeline; see goodjob in the google console
    pipeline.run()


if __name__ == '__main__':
    run()
