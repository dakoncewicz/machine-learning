#!/usr/bin/env python


import apache_beam as beam
import re
import sys

def custom_grep(line, search_query):

   if re.match( r'^' + re.escape(search_query), line):

      yield line

if __name__ == '__main__':

   pipeline = beam.Pipeline(argv=sys.argv)

   input = './java/*.java'

   output_prefix = './tmp/grep_pipeline_output'

   search_query = 'import'

   (pipeline
      | 'GetInput' >> beam.io.ReadFromText(input)
      | 'Grep' >> beam.FlatMap(lambda line: custom_grep(line, search_query))
      | 'WriteOutput' >> beam.io.WriteToText(output_prefix)
   )

   pipeline.run().wait_until_finish()
