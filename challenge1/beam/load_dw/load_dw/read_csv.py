
import io
import sys
import csv
import apache_beam as beam
import apache_beam.io.fileio


def _parse_csv(readable_file):
    """Parse file as CSV

    :param readable_file: Readable file
    """
    if sys.version_info >= (3, 0):
        file = io.TextIOWrapper(readable_file.open())
    else:
        file = readable_file.open()
    return csv.DictReader(file)


class ReadCSV(beam.PTransform):
    """Transform for opening csv files

    :param file_pattern: File pattern
    :type file_pattern: str
    """

    def __init__(self, file_pattern):
        super().__init__()
        self.file_pattern = file_pattern

    def expand(self, p):
        return (p
                | 'search_files' >> beam.io.fileio.MatchFiles(file_pattern=self.file_pattern)
                | 'read_files' >> beam.io.fileio.ReadMatches()
                | 'parse_csv' >> beam.FlatMap(_parse_csv))
