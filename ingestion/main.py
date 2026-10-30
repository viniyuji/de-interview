import argparse
import csv
import io
import logging
import sys
from pathlib import Path

import psycopg2

NULL_TOKENS = {"", "NA"}

# Child tables first so a rerun can clear rows without breaking foreign keys.
DELETE_ORDER = ("flights", "weather", "planes", "airports", "airlines")

LOADS = (
    {
        "table": "airlines",
        "file": "nyc_airlines.csv",
        "columns": ("carrier", "name"),
    },
    {
        "table": "airports",
        "file": "nyc_airports.csv",
        "columns": (
            "faa",
            "name",
            "latitude",
            "longitude",
            "altitude",
            "timezone",
            "dst",
            "timezone_name",
        ),
        "rename": {
            "lat": "latitude",
            "lon": "longitude",
            "alt": "altitude",
            "tz": "timezone",
            "tzone": "timezone_name",
        },
    },
    {
        "table": "planes",
        "file": "nyc_planes.csv",
        "columns": (
            "tailnum",
            "year",
            "type",
            "manufacturer",
            "model",
            "engines",
            "seats",
            "speed",
            "engine",
        ),
    },
    {
        "table": "weather",
        "file": "nyc_weather.csv",
        "columns": (
            "origin",
            "year",
            "month",
            "day",
            "hour",
            "temp",
            "dewp",
            "humid",
            "wind_dir",
            "wind_speed",
            "wind_gust",
            "precip",
            "pressure",
            "visib",
            "time_hour",
        ),
        "dedupe_key": ("origin", "year", "month", "day", "hour"),
    },
    {
        "table": "flights",
        "file": "nyc_flights.csv",
        "columns": (
            "carrier",
            "flight",
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "actual_dep_time",
            "sched_dep_time",
            "dep_delay",
            "actual_arr_time",
            "sched_arr_time",
            "arr_delay",
            "tailnum",
            "origin",
            "dest",
            "air_time",
            "distance",
            "time_hour",
        ),
        "rename": {
            "dep_time": "actual_dep_time",
            "arr_time": "actual_arr_time",
        },
    },
)


def _parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=5432)
    parser.add_argument("--user", default="de_challenge")
    parser.add_argument("--password", default="Password1234**")
    parser.add_argument("--database", default="bronze_csv")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "challenge1" / "dataset",
    )
    return parser.parse_args(argv)


def _cell(value):
    if value is None or value.strip() in NULL_TOKENS:
        return ""
    return value.strip()


def _read_rows(path, columns, rename=None, dedupe_key=None):
    rename = rename or {}
    rows = []
    seen = {}
    duplicates = 0

    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for source in reader:
            mapped = {}
            for source_name, value in source.items():
                if not source_name:
                    continue
                mapped[rename.get(source_name, source_name)] = _cell(value)
            row = [mapped.get(column, "") for column in columns]
            if dedupe_key:
                key = tuple(mapped[column] for column in dedupe_key)
                if key in seen:
                    duplicates += 1
                seen[key] = row
            else:
                rows.append(row)

    if dedupe_key:
        rows = list(seen.values())
        if duplicates:
            logging.info(
                "Collapsed %s duplicate %s rows on %s, keeping the latest row",
                duplicates,
                path.name,
                ", ".join(dedupe_key),
            )
    return rows


def _copy_rows(cursor, table, columns, rows):
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerows(rows)
    buffer.seek(0)
    column_list = ", ".join(columns)
    cursor.copy_expert(
        f"COPY public.{table} ({column_list}) FROM STDIN WITH (FORMAT csv, NULL '')",
        buffer,
    )
    logging.info("Loaded %s rows into %s", len(rows), table)


def load(args):
    dataset = args.dataset.resolve()
    if not dataset.is_dir():
        raise FileNotFoundError(f"Dataset directory not found: {dataset}")

    connection = psycopg2.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        dbname=args.database,
    )
    try:
        with connection:
            with connection.cursor() as cursor:
                for table in DELETE_ORDER:
                    cursor.execute(f"DELETE FROM public.{table}")
                for spec in LOADS:
                    path = dataset / spec["file"]
                    rows = _read_rows(
                        path,
                        spec["columns"],
                        rename=spec.get("rename"),
                        dedupe_key=spec.get("dedupe_key"),
                    )
                    _copy_rows(cursor, spec["table"], spec["columns"], rows)
                cursor.execute(
                    """
                    SELECT 'airlines', COUNT(*) FROM public.airlines
                    UNION ALL SELECT 'airports', COUNT(*) FROM public.airports
                    UNION ALL SELECT 'planes', COUNT(*) FROM public.planes
                    UNION ALL SELECT 'weather', COUNT(*) FROM public.weather
                    UNION ALL SELECT 'flights', COUNT(*) FROM public.flights
                    ORDER BY 1
                    """
                )
                for table, count in cursor.fetchall():
                    logging.info("public.%s now has %s rows", table, count)
        logging.info("Committed load into %s", args.database)
    finally:
        connection.close()


def main(argv=None):
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    load(_parse_args(sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    main()
