
import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from beam_nuggets.io.relational_db import TableConfiguration, SourceConfiguration


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dest_host', dest='dest_host', type=str)
    parser.add_argument('--dest_port', dest='dest_port', type=int)
    parser.add_argument('--dest_username', dest='dest_username', type=str)
    parser.add_argument('--dest_password', dest='dest_password', type=str)
    parser.add_argument('--dest_database', dest='dest_database', type=str)
    parser.add_argument('--dest_table', dest='dest_table', type=str)
    parser.add_argument('--source', dest='source', type=str)
    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options = PipelineOptions(pipeline_args)

    with beam.Pipeline(options=pipeline_options) as p:
        table_name = known_args.dest_table
        db_configuration = SourceConfiguration(
            drivername='postgresql',
            host=known_args.dest_host,
            port=known_args.dest_port,
            username=known_args.dest_username,
            password=known_args.dest_password,
            database=known_args.dest_database,
        )
        table_configuration = TableConfiguration(
            name=table_name,
            create_if_missing=False
        )

        # Develop main pipeline
