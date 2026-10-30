
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
    parser.add_argument('--source', dest='source', type=str)
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


def _get_source_path(source):
    """Build absolute source file path

    :param source Source path
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_path, source)


def main(argv):
    try:
        config = _get_config(argv)
        conn, cursor = _connect_db(config)
        source_path = _get_source_path(config.source)

        try:
            with open(source_path, 'r') as f:
                columns = []
            conn.commit()
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main(sys.argv)
