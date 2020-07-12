from argparse import ArgumentParser
from datetime import datetime, timezone
import json
import os
import re
import sys
import time
import uuid

from kafka import KafkaProducer, KafkaConsumer
import psycopg2 as pg
import requests


API_VERSION_AUTO_TIMEOUT_MS = 5000


def check_website(url, regexp):
    t1 = time.time()
    r = requests.get(url, timeout=1.0)
    t2 = time.time()
    if r.status_code == 200 and regexp is not None:
        regexp_matched = re.search(regexp, r.text) is not None
    else:
        regexp_matched = None
    return {
        'ts': str(datetime.now(timezone.utc)),
        'url': url,
        'response_time_ms': int((t2 - t1) * 1000),
        'http_status_code': r.status_code,
        'regexp': regexp,
        'regexp_matched': regexp_matched,
    }

def run_producer(kafka_urls, topic, website_url, regexp, cafile, certfile, keyfile):
    producer = KafkaProducer(
        api_version_auto_timeout_ms=API_VERSION_AUTO_TIMEOUT_MS,
        bootstrap_servers=kafka_urls,
        security_protocol="SSL",
        ssl_cafile=cafile,
        ssl_certfile=certfile,
        ssl_keyfile=keyfile,
    )
    while True:
        msg = check_website(website_url, regexp)
        print('sending {}'.format(msg))
        producer.send(topic, json.dumps(msg).encode())
        producer.flush()
        time.sleep(5)


def run_consumer(kafka_urls, topic, db_url, cafile, certfile, keyfile):
    consumer = KafkaConsumer(
        topic,
        api_version_auto_timeout_ms=API_VERSION_AUTO_TIMEOUT_MS,
        auto_offset_reset="earliest",
        bootstrap_servers=kafka_urls,
        client_id="demo-client-1",
        group_id="demo-group",
        security_protocol="SSL",
        ssl_cafile=cafile,
        ssl_certfile=certfile,
        ssl_keyfile=keyfile,
    )
    while True:
        raw_msgs = consumer.poll(timeout_ms=5000)
        if raw_msgs:
            with pg.connect(db_url) as conn:
                with conn.cursor() as cur:
                    for tp, msgs in raw_msgs.items():
                        for msg in msgs:
                            print("Received: {} : {}".format(tp, msg.value))
                            msg = json.loads(msg.value)
                            cur.execute('''
                                insert into site_avail_stats (
                                    ts, url, response_time_ms, http_status_code, regexp, regexp_matched
                                ) values (
                                    %(ts)s,
                                    %(url)s,
                                    %(response_time_ms)s,
                                    %(http_status_code)s,
                                    %(regexp)s,
                                    %(regexp_matched)s
                                )''', msg)
                    conn.commit()
                    consumer.commit() # TODO: commit each processed message individually
        else:
            print('No new messages so far')


def main():
    parser = ArgumentParser('Monitor a website availability.')
    parser.add_argument('action', choices=['produce', 'consume'], help='Start a kafka producer or a kafka consumer')
    parser.add_argument('-k', '--kafka-url', action='append', help='Kafka broker url, can be specified multiple times')
    parser.add_argument('-d', '--db-url', help='Database URL')
    parser.add_argument('-t', '--topic', help='Kafka topic')
    parser.add_argument('-w', '--website-url', help='URL of the website to monitor')
    parser.add_argument('-r', '--regexp', help='An optional regexp to match against the website content')
    parser.add_argument('--cafile', help='Path to SSL CA file', default='ca.pem')
    parser.add_argument('--certfile', help='Path to SSL certificate file', default='service.cert')
    parser.add_argument('--keyfile', help='Path to SSL key file', default='service.key')
    parser.add_argument('--kafka-client-id', help='Kafka client id', default='demo-client-1')
    parser.add_argument('--kafka-group-id', help='Kafka group id', default='demo-group')

    args = parser.parse_args()
    print(args)

    if args.action == 'produce':
        run_producer(
            args.kafka_url,
            args.topic,
            args.website_url,
            args.regexp,
            args.cafile,
            args.certfile,
            args.keyfile,
        )
    elif args.action == 'consume':
        run_consumer(
            args.kafka_url,
            args.topic,
            args.db_url,
            args.cafile,
            args.certfile,
            args.keyfile,
        )

if __name__ == '__main__':
    main()

