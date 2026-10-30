
import apache_beam as beam


def _map_to_csv(element, columns, delimiter):
    """Map each element to CSV format

    :param element: Collection element
    :param columns: Columns to save in the CSV file
    :param delimiter: CSV file delimiter
    """

    def _parse_column(column):
        """Parse column value to CSV format

        :param column: key name of the column
        """

        value = '' if element[column] is None else str(element[column])
        return f'"{value}"'

    return delimiter.join([_parse_column(column) for column in columns])


class WriteToCSV(beam.PTransform):
    """Transform for writing CSV files

    :param file_path_prefix: File path
    :param columns: : Columns to save in the CSV file
    :param delimiter: CSV file delimiter
    """

    def __init__(self, file_path_prefix, columns, delimiter=',', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.file_path_prefix = file_path_prefix
        self.columns = columns
        self.delimiter = delimiter

    def expand(self, p):
        return (p
                | 'map_to_csv' >> beam.Map(
                    _map_to_csv,
                    self.columns,
                    self.delimiter)
                | 'write_csv' >> beam.io.WriteToText(
                    self.file_path_prefix,
                    shard_name_template='',
                    header=','.join(self.columns)))
