-- CREATE NON ROOT USER

CREATE USER de_challenge WITH ENCRYPTED PASSWORD 'Password1234**';
GRANT ALL PRIVILEGES ON DATABASE dw_flights TO de_challenge;
GRANT ALL ON ALL TABLES IN SCHEMA public TO de_challenge;

---- Drop user if needed
-- DROP OWNED BY de_challenge;
-- DROP USER de_challenge;

-- Create DW Tables

CREATE TABLE airlines(
    carrier VARCHAR(2),
    name VARCHAR NOT NULL,
    CONSTRAINT p_airline PRIMARY KEY (carrier)
);

CREATE TABLE airports(
    faa VARCHAR(3),
    name VARCHAR NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    altitude FLOAT NOT NULL,
    timezone INTEGER NOT NULL,
    dst VARCHAR(1) NOT NULL,
    timezone_name VARCHAR NOT NULL,
    CONSTRAINT p_airport PRIMARY KEY (faa)
);

CREATE TABLE planes(
    tailnum VARCHAR(6),
    year INTEGER,
    type VARCHAR NOT NULL,
    manufacturer VARCHAR NOT NULL,
    model VARCHAR NOT NULL,
    engines INTEGER NOT NULL,
    seats INTEGER NOT NULL,
    speed FLOAT,
    engine VARCHAR NOT NULL,
    CONSTRAINT p_plane PRIMARY KEY (tailnum)
);

CREATE TABLE weather(
    origin VARCHAR(3),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    hour INTEGER NOT NULL,
    temp NUMERIC,
    dewp NUMERIC,
    humid NUMERIC,
    wind_dir FLOAT,
    wind_speed NUMERIC,
    wind_gust NUMERIC,
    precip NUMERIC,
    pressure NUMERIC,
    visib NUMERIC,
    time_hour TIMESTAMPTZ NOT NULL,
    CONSTRAINT p_weather PRIMARY KEY (origin, year, month, day, hour),
    CONSTRAINT fk_airport FOREIGN KEY (origin) REFERENCES airports(faa)
);

CREATE TABLE flights(
    carrier VARCHAR(2),
    flight INTEGER NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    hour INTEGER NOT NULL,
    minute INTEGER NOT NULL,
    actual_dep_time INTEGER,
    sched_dep_time INTEGER,
    dep_delay INTEGER,
    actual_arr_time INTEGER,
    sched_arr_time INTEGER,
    arr_delay INTEGER,
    tailnum	VARCHAR(6) NOT NULL,
    origin	VARCHAR(3) NOT NULL,
    dest VARCHAR(3) NOT NULL,
    air_time FLOAT NOT NULL,
    distance FLOAT NOT NULL,
    time_hour TIMESTAMPTZ NOT NULL,
    CONSTRAINT p_flight PRIMARY KEY (carrier, flight, year, month, day, hour, minute),
    CONSTRAINT fk_airline FOREIGN KEY (carrier) REFERENCES airlines(carrier),
    CONSTRAINT fk_plane FOREIGN KEY (tailnum) REFERENCES planes(tailnum),
    CONSTRAINT fk_origin FOREIGN KEY (origin) REFERENCES airports(faa),
    CONSTRAINT fk_dest FOREIGN KEY (dest) REFERENCES airports(faa)
);
