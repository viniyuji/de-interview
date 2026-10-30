
import os
import sys
import argparse
import logging
import psycopg2
import psycopg2.extras


def _get_config(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', type=str)
    parser.add_argument('--port', dest='port', type=int)
    parser.add_argument('--username', dest='username', type=str)
    parser.add_argument('--password', dest='password', type=str)
    parser.add_argument('--database', dest='database', type=str)
    parser.add_argument('--table', dest='table', type=str)
    parser.add_argument('--destination', dest='destination', type=str)
    parser.add_argument('--delimiter', dest='delimiter', type=str, default=',')
    config, _ = parser.parse_known_args(argv)

    return config


def _connect_db(config):
    """Create database connection

    :param config Configuration parameters
    """
    conn = psycopg2.connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    return conn, cursor


def _get_destination_path(source):
    """Build absolute source file path

    :param source Source path
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_path, source)


def _get_table_columns():
    # hint: select just one record from the table and extract its keys
    row = {}
    return list(row.keys())


def main(argv):
    try:
        config = _get_config(argv)
        conn, cursor = _connect_db(config)
        destination_path = _get_destination_path(config.destination)

        try:
            with open(destination_path, 'w') as f:
                columns = []
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main(sys.argv)
