# webmon
A sample tool to monitor a website availability.

## Installation
The tool requires Python3 (it was tested with Python 3.7.6).
The package depends on psycopg2, which in turn depends on PostgreSQL client library, so the latter should be installed prior to the next step.
Then use standard means to install the webmon Python package, e.g.:
```bash
pip install -e git+https://github.com/filindm/webmon#egg=webmon
```
Then view the built-in help:
```bash
webmon --help
```

## Prerequisites
This tool requires:
- A topic in Kafka. The name of the topic will then need to be specified as command line argument to `webmon`. 
- A table in PostgreSQL, see the schema here: https://github.com/filindm/webmon/blob/master/create_db_schema.sql. You might want to add some indexes to the table to allow for an efficient lookup, depending on your applications needs.
- CA file, SSL certificate and key file. Default file paths are ./ca.pem, ./service.cert and ./service.key. Alternate locations can be specified via command line arguments.

## How to run
The tool consists of two components - producer and consumer. 
Producer peridically checks the target website and sends the check results to a Kafka topic. 
Consumer subscribes to the same topic and stores the results in a PostgreSQL database.
Example:
```bash
webmon consume -k <Kafka URL> -t test-topic-1 -d <PostgreSQL URL>

webmon produce -k <Kafka URL> -t test-topic-1 -w https://aiven.io -r Aiven
```

## Know issues and limitations
- The tool currently supports only SSL for both Kafka and PostgreSQL.
