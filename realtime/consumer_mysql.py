import argparse
import json
import os
import time
from datetime import datetime, timezone

import pymysql
from kafka import KafkaConsumer


DEFAULT_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
DEFAULT_TOPIC = os.environ.get("CITIBIKE_STATION_STATUS_TOPIC", "citibike.station_status")


UPSERT_SQL = """
INSERT INTO citibike_station_status_stream (
  station_id,
  observed_at,
  source_url,
  feed_last_updated,
  num_bikes_available,
  num_docks_available,
  is_installed,
  is_renting,
  is_returning,
  station_last_reported,
  kafka_topic,
  kafka_partition,
  kafka_offset,
  raw_payload
) VALUES (
  %(station_id)s,
  %(observed_at)s,
  %(source_url)s,
  FROM_UNIXTIME(%(feed_last_updated)s),
  %(num_bikes_available)s,
  %(num_docks_available)s,
  %(is_installed)s,
  %(is_renting)s,
  %(is_returning)s,
  FROM_UNIXTIME(%(last_reported)s),
  %(kafka_topic)s,
  %(kafka_partition)s,
  %(kafka_offset)s,
  %(raw_payload)s
)
ON DUPLICATE KEY UPDATE
  observed_at = VALUES(observed_at),
  source_url = VALUES(source_url),
  feed_last_updated = VALUES(feed_last_updated),
  num_bikes_available = VALUES(num_bikes_available),
  num_docks_available = VALUES(num_docks_available),
  is_installed = VALUES(is_installed),
  is_renting = VALUES(is_renting),
  is_returning = VALUES(is_returning),
  station_last_reported = VALUES(station_last_reported),
  kafka_topic = VALUES(kafka_topic),
  kafka_partition = VALUES(kafka_partition),
  kafka_offset = VALUES(kafka_offset),
  raw_payload = VALUES(raw_payload),
  updated_at = CURRENT_TIMESTAMP
"""


def mysql_connection():
    return pymysql.connect(
        host=os.environ.get("MYSQL_HOST", "mysql"),
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        user=os.environ.get("MYSQL_USER", "testuser"),
        password=os.environ.get("MYSQL_PASSWORD", "testpass"),
        database=os.environ.get("MYSQL_DATABASE", "testdb"),
        autocommit=False,
        charset="utf8mb4",
    )


def normalize_timestamp(value):
    if not value:
        return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
    return str(value).replace("T", " ").replace("+00:00", "").replace("Z", "")


def to_int_or_none(value):
    if value is None or value == "":
        return None
    return int(value)


def consume(args):
    consumer = KafkaConsumer(
        args.topic,
        bootstrap_servers=args.bootstrap_servers,
        group_id=args.group_id,
        auto_offset_reset=args.offset_reset,
        enable_auto_commit=True,
        consumer_timeout_ms=args.timeout_ms,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )
    conn = mysql_connection()
    consumed = 0
    started = time.time()

    try:
        with conn.cursor() as cursor:
            for record in consumer:
                payload = record.value
                params = {
                    "station_id": str(payload.get("station_id", "")).strip(),
                    "observed_at": normalize_timestamp(payload.get("observed_at")),
                    "source_url": payload.get("source_url", ""),
                    "feed_last_updated": to_int_or_none(payload.get("feed_last_updated")),
                    "num_bikes_available": to_int_or_none(payload.get("num_bikes_available")),
                    "num_docks_available": to_int_or_none(payload.get("num_docks_available")),
                    "is_installed": to_int_or_none(payload.get("is_installed")),
                    "is_renting": to_int_or_none(payload.get("is_renting")),
                    "is_returning": to_int_or_none(payload.get("is_returning")),
                    "last_reported": to_int_or_none(payload.get("last_reported")),
                    "kafka_topic": record.topic,
                    "kafka_partition": record.partition,
                    "kafka_offset": record.offset,
                    "raw_payload": json.dumps(payload, separators=(",", ":")),
                }
                if not params["station_id"]:
                    continue
                cursor.execute(UPSERT_SQL, params)
                consumed += 1
                if consumed % args.commit_every == 0:
                    conn.commit()
                if args.max_messages and consumed >= args.max_messages:
                    break
                if args.max_seconds and (time.time() - started) >= args.max_seconds:
                    break
            conn.commit()
    finally:
        consumer.close()
        conn.close()

    print(f"consumed_records={consumed} topic={args.topic} group_id={args.group_id}")
    return consumed


def main():
    parser = argparse.ArgumentParser(description="Consume Citi Bike Kafka station status into MySQL.")
    parser.add_argument("--bootstrap-servers", default=DEFAULT_BOOTSTRAP)
    parser.add_argument("--topic", default=DEFAULT_TOPIC)
    parser.add_argument("--group-id", default=os.environ.get("REALTIME_CONSUMER_GROUP", "citibike-station-status-mysql"))
    parser.add_argument("--offset-reset", default=os.environ.get("REALTIME_OFFSET_RESET", "latest"))
    parser.add_argument("--timeout-ms", type=int, default=int(os.environ.get("REALTIME_CONSUMER_TIMEOUT_MS", "1000")))
    parser.add_argument("--max-messages", type=int, default=0)
    parser.add_argument("--max-seconds", type=int, default=0)
    parser.add_argument("--commit-every", type=int, default=100)
    parser.add_argument("--loop", action="store_true")
    args = parser.parse_args()

    while True:
        consume(args)
        if not args.loop:
            break
        time.sleep(1)


if __name__ == "__main__":
    main()
