#############################################################################
# for your convenience run below Python code in Google Colab environment
# goto https://colab.research.google.com/
#
# in colab install the apache_beam package
# !{'pip install --quiet apache_beam'}
#
# next, create directory for data files
# !{'mkdir -p data'}
#
# finaly, upload your local file to the colab
# from google.colab import files
# uplad = files.upload()
#
# Now, you are ready to start work with your python apache_beam examples
############################################################################

import apache_beam as beam
import re

INPUT_PATTERN = 'gs://dataflow-samples/shakespeare/kinglear.txt'
OUTPUT_PREFIX = 'outputs/count'


def SplitRow(line):
    return re.split(r"[\s,.-?;]", line)


# step 1 Creating and giving pipeline a name
p1 = beam.Pipeline()

attendance_count = (

    p1
    # Step2 Initial Pcollection by reading data from a source
    | 'Read lines' >> beam.io.ReadFromText(INPUT_PATTERN)
    # Step 3 Ptransformation according to requirements
    | 'Find words' >> beam.FlatMap(SplitRow)
    | 'lowercase' >> beam.Map(lambda word: str.lower(word))
    | 'Pair words with counter' >> beam.Map(lambda word: (word, 1))
    | 'Group and sum' >> beam.CombinePerKey(sum)
    | 'Format results' >> beam.Map(lambda word_count: str(word_count))
    # Step 4 Write Pcollection to a sink
    | 'Write results' >> beam.io.WriteToText(OUTPUT_PREFIX)

)

# Step 5 Run the pipeline
p1.run()

# Sample the first 20 results, remember there are no ordering guarantees.
#!{('head -n 20 {}-00000-of-*'.format(OUTPUT_PREFIX)}
