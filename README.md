# Data Engineer Coding Exercise

This project consists of the basic tools needed to solve BEON's Data Engineer Exercise. It contains a New York City flights dataset, a documents collection, instructions for deploying the required database (PostgreSQL), and pre-developed projects that may help you to save time.

## Set the environment

For developing the first challenge, you will need to set an ETL tool and a PostgreSQL database. You can use whatever tool you feel most comfortable in. Using an SQL database is the only requirement.

### Set the database

You can deploy your database using Docker and the official PostgreSQL image by using the following command.

```bash
docker run \
--name de_challenge2 \
-e POSTGRES_PASSWORD="Password1234**" \
-e POSTGRES_DB=dw_flights \
-v ${PWD}/init_db.sql:/docker-entrypoint-initdb.d/init_db.sql \
-p 5432:5432 \
-d postgres
```

The `init_db.sql` file will be run at database startup for creating the user for connecting to the database and creating the required tables. Once the database has started, it is ready to use with all the necessary structures.

## What does the coding exercise look like?

The coding exercise is a pair programming session where we will request you to develop an ETL pipeline using whatever tool you feel most comfortable in and a small search application (prototype), solve bugs, or give code advice. You will be able to use Google and any documentation that can help you. Instructions will be provided in the live coding session.

*Please, take a look at the datasets in order to understand the data provided. It will help you to save time.*

## Requirements

- Your preferred IDE / Code Editor, e.g., Pycharm, Visual Studio Code, Sublime Text, Atom.
- Your preferred programming language, e.g., Python, Node, Go, PHP. You can even use Visual Basic if you want.
- SQL Client, e.g., DataGrip, pgAdmin 4, SQL Server Management Studio, DBeaver.
- PostgreSQL database. You can deploy it wherever you want, e.g., Docker, locally, AWS, GCP.
- Your preferred ETL tools, e.g., Apache Beam, Apache Spark, dbt.

## Credits

The NYC Flights 2013 dataset published by [aephidayatuloh](https://www.kaggle.com/aephidayatuloh) was extracted from [Kaggle](https://www.kaggle.com/aephidayatuloh/nyc-flights-2013).
