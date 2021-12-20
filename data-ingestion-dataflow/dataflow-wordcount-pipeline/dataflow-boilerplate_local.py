##################################################################################
# This is the Bolierplate code which helps you to run local Python dataflow code
# in Google Cloud Cloud Shell using command line parameters
#
##################################################################################

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import argparse

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

# step 1 Creating and giving pipeline a name
options = PipelineOptions(pipeline_args)
p = beam.Pipeline(options=options)

attendance_count = (
    p
    # Step2 Initial Pcollection by reading data from a source passed as cmd parametr  --input
    | 'Read lines' >> beam.io.ReadFromText(inputs_pattern)
    # Step 3 samples Ptransformation according to requirements - put your code instead of this sample up to Step 4
    | 'Split row' >> beam.Map(lambda record: record.split(','))
    | 'Get all Accounts Dept Persons' >> beam.Filter(lambda record: record[3] == 'Accounts')
    | 'Pair each employee with 1' >> beam.Map(lambda record: (record[1], 1))
    | 'Group and sum' >> beam.CombinePerKey(sum)
    | 'Format results' >> beam.Map(lambda employee_count: str(employee_count))
    # Step 4 Write Pcollection to a sink text file accordin the parameters passed in cmd line as --output
    | 'Write results' >> beam.io.WriteToText(outputs_prefix)
)

# Step 5 Run the pipeline
p.run()
