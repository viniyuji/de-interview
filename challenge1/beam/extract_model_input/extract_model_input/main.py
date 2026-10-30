
import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from beam_nuggets.io.relational_db import SourceConfiguration


CSV_COLUMNS = [
    'airline',
    'flight',
    'flight_date',
    'tailnum',
    'sched_dep_time',
    'actual_dep_time',
    'dep_delay',
    'sched_arr_time',
    'actual_arr_time',
    'arr_delay',
    'origin_faa',
    'origin_name',
    'origin_latitude',
    'origin_longitude',
    'origin_altitude',
    'origin_temp',
    'origin_dewp',
    'origin_humid',
    'origin_precip',
    'origin_pressure',
    'origin_visib',
    'dest_faa',
    'dest_name',
    'dest_latitude',
    'dest_longitude',
    'dest_altitude',
    'air_time',
    'distance',
    'airplane_model',
    'airplane_seats'
]


def _map_airline(airline):
    return airline['carrier'], airline['name']


def _map_airport(kv, prefix):
    key, airport = kv
    data = {
        f'{prefix}_faa': airport['faa'],
        f'{prefix}_name': airport['name'],
        f'{prefix}_latitude': airport['latitude'],
        f'{prefix}_longitude': airport['longitude'],
        f'{prefix}_altitude': airport['altitude'],
    }
    return key, data


def _map_plane(plane):
    data = {
        'airplane_model': None,
        'airplane_seats': None
    }
    return plane['tailnum'], data


def _map_weather(weather):
    data = {
        'origin_temp': weather['temp'],
        'origin_dewp': weather['dewp'],
        'origin_humid': weather['humid'],
        'origin_precip': weather['precip'],
        'origin_pressure': weather['pressure'],
        'origin_visib': weather['visib']
    }
    origin = weather['origin']
    year = weather['year']
    month = weather['month']
    day = weather['day']
    hour = weather['hour']
    return weather_key, data


def _map_flight(flight):

    def _parse_time(time):
        text_time = str(time)
        hour = text_time.zfill(2)
        minute = text_time.zfill(2)
        return f'{hour}:{minute}'

    sched_dep_time = _parse_time(flight['sched_dep_time'])
    actual_dep_time = _parse_time(flight['actual_dep_time'])
    sched_arr_time = _parse_time(flight['sched_arr_time'])
    actual_arr_time = _parse_time(flight['actual_arr_time'])

    return {
        'airline': flight['carrier'],
        'flight': flight_name,
        'flight_date': flight_date,
        'tailnum': flight['tailnum'],
        'origin_faa': flight['origin'],
        'dest_faa': flight['dest'],
        'air_time': flight['air_time'],
        'distance': flight['distance'],

        'sched_dep_time': sched_dep_time,
        'actual_dep_time': actual_dep_time,
        'dep_delay': flight['dep_delay'],

        'sched_arr_time': sched_arr_time,
        'actual_arr_time': actual_arr_time,
        'arr_delay': flight['arr_delay']
    }


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_host', dest='source_host', type=str)
    parser.add_argument('--source_port', dest='source_port', type=int)
    parser.add_argument('--source_username', dest='source_username', type=str)
    parser.add_argument('--source_password', dest='source_password', type=str)
    parser.add_argument('--source_database', dest='source_database', type=str)
    parser.add_argument('--dest', dest='dest', type=str)
    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options = PipelineOptions(pipeline_args)

    with beam.Pipeline(options=pipeline_options) as p:
        db_configuration = SourceConfiguration(
            drivername='postgresql',
            host=known_args.source_host,
            port=known_args.source_port,
            username=known_args.source_username,
            password=known_args.source_password,
            database=known_args.source_database,
        )

        # Develop main pipeline
