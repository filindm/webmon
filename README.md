# webmon
A sample tool to monitor a website availability.

## Installation
```bash
pip install -e git+https://github.com/filindm/webmon#egg=webmon
```
Then view the built-in help:
```bash
webmon --help
```

## How to run
The tool consists of two components - producer and consumer. 
Producer peridically checks the target website and sends the check results to a Kafka topic. 
Consumer subscribes to the same topic and stores the results in a PostgreSQL database.
Example:
```bash
webmon consume -k <Kafka URL> -t test-topic-1 -d <PostgreSQL URL>

webmon produce -k <Kafka URL> -t test-topic-1 -w https://aiven.io -r Aiven
```
