SELECT
    airlines.name AS airline,
    flights.carrier || '-' || flights.flight::varchar AS flight,
    make_date(flights.year, flights.month, flights.day) AS flight_date,
    flights.tailnum,
    substring(lpad(flights.sched_dep_time::varchar, 4, '0'), 1, 2)
        || ':'
        || substring(lpad(flights.sched_dep_time::varchar, 4, '0'), 3, 2) AS sched_dep_time,
    substring(lpad(flights.actual_dep_time::varchar, 4, '0'), 1, 2)
        || ':'
        || substring(lpad(flights.actual_dep_time::varchar, 4, '0'), 3, 2) AS actual_dep_time,
    flights.dep_delay,
    substring(lpad(flights.sched_arr_time::varchar, 4, '0'), 1, 2)
        || ':'
        || substring(lpad(flights.sched_arr_time::varchar, 4, '0'), 3, 2) AS sched_arr_time,
    substring(lpad(flights.actual_arr_time::varchar, 4, '0'), 1, 2)
        || ':'
        || substring(lpad(flights.actual_arr_time::varchar, 4, '0'), 3, 2) AS actual_arr_time,
    flights.arr_delay,
    origin.faa AS origin_faa,
    origin.name AS origin_name,
    origin.latitude AS origin_latitude,
    origin.longitude AS origin_longitude,
    origin.altitude AS origin_altitude,
    weather.temp AS origin_temp,
    weather.dewp AS origin_dewp,
    weather.humid AS origin_humid,
    weather.precip AS origin_precip,
    weather.pressure AS origin_pressure,
    weather.visib AS origin_visib,
    destination.faa AS dest_faa,
    destination.name AS dest_name,
    destination.latitude AS dest_latitude,
    destination.longitude AS dest_longitude,
    destination.altitude AS dest_altitude,
    flights.air_time,
    flights.distance,
    trim(planes.manufacturer) || ' ' || trim(planes.model) AS airplane_model,
    planes.seats AS airplane_seats
FROM {{ source('raw', 'flights') }} AS flights
LEFT JOIN {{ source('raw', 'airlines') }} AS airlines
    ON flights.carrier = airlines.carrier
LEFT JOIN {{ source('raw', 'airports') }} AS origin
    ON flights.origin = origin.faa
LEFT JOIN {{ source('raw', 'airports') }} AS destination
    ON flights.dest = destination.faa
LEFT JOIN {{ source('raw', 'planes') }} AS planes
    ON flights.tailnum = planes.tailnum
LEFT JOIN {{ source('raw', 'weather') }} AS weather
    ON flights.origin = weather.origin
    AND flights.year = weather.year
    AND flights.month = weather.month
    AND flights.day = weather.day
    AND flights.hour = weather.hour
