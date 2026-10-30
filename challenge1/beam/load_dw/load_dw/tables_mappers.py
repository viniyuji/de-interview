
def _map_null_value(value):
    return None if value == 'NA' else value

def _map_airport(row):
    return {
        'faa': row['faa'],
        'name': row['name'],
        'latitude': row['lat'],
        'longitude': row['lon'],
        'altitude': row['alt'],
        'timezone': row['tz'],
        'dst': row['dst'],
        'timezone_name': row['tzone']
    }


def _map_plane(row):
    return {
        **row,
        'year': _map_null_value(row['year']),
        'speed': _map_null_value(row['speed'])
    }


def _map_weather(row):
    return {
        **row,
        'temp': _map_null_value(row['temp']),
        'dewp': _map_null_value(row['dewp']),
        'humid': _map_null_value(row['humid']),
        'wind_dir': _map_null_value(row['wind_dir']),
        'wind_speed': _map_null_value(row['wind_speed']),
        'wind_gust': _map_null_value(row['wind_gust']),
        'precip': _map_null_value(row['precip']),
        'pressure': _map_null_value(row['pressure']),
        'visib': _map_null_value(row['visib'])
    }


def _map_flight(row):
    return {
        'carrier': row['carrier'],
        'flight': row['flight'],
        'year': row['year'],
        'month': row['month'],
        'day': row['day'],
        'hour': row['hour'],
        'minute': row['minute'],
        'actual_dep_time': row['dep_time'],
        'schedule_dep_time': row['sched_dep_time'],
        'dep_delay': row['dep_delay'],
        'actual_arr_time': row['arr_time'],
        'sched_arr_time': row['sched_arr_time'],
        'arr_delay': row['arr_delay'],
        'tailnum': row['tailnum'],
        'origin': row['origin'],
        'dest': row['dest'],
        'air_time': row['air_time'],
        'distance': row['distance'],
        'time_hour': row['time_hour']
    }
