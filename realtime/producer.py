import argparse
import json
import os
import time
from datetime import datetime, timezone

import requests
from kafka import KafkaProducer


DEFAULT_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
DEFAULT_TOPIC = os.environ.get("CITIBIKE_STATION_STATUS_TOPIC", "citibike.station_status")
DEFAULT_URL = os.environ.get(
    "CITIBIKE_STATION_STATUS_URL",
    "https://gbfs.citibikenyc.com/gbfs/2.3/en/station_status.json",
)


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def fetch_station_status(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    payload = response.json()
    stations = payload.get("data", {}).get("stations", [])
    ttl = payload.get("ttl")
    last_updated = payload.get("last_updated")
    return stations, ttl, last_updated


def publish_once(producer, topic, url, max_records):
    observed_at = utc_now()
    stations, ttl, feed_last_updated = fetch_station_status(url)
    if max_records > 0:
        stations = stations[:max_records]

    for station in stations:
        station_id = str(station.get("station_id", "")).strip()
        if not station_id:
            continue
        message = {
            "event_type": "station_status",
            "observed_at": observed_at,
            "source_url": url,
            "feed_ttl": ttl,
            "feed_last_updated": feed_last_updated,
            "station_id": station_id,
            "num_bikes_available": station.get("num_bikes_available"),
            "num_docks_available": station.get("num_docks_available"),
            "is_installed": station.get("is_installed"),
            "is_renting": station.get("is_renting"),
            "is_returning": station.get("is_returning"),
            "last_reported": station.get("last_reported"),
        }
        producer.send(topic, key=station_id.encode("utf-8"), value=message)

    producer.flush()
    print(f"published_records={len(stations)} topic={topic} observed_at={observed_at}")
    return len(stations)


def main():
    parser = argparse.ArgumentParser(description="Publish Citi Bike GBFS station status to Kafka.")
    parser.add_argument("--bootstrap-servers", default=DEFAULT_BOOTSTRAP)
    parser.add_argument("--topic", default=DEFAULT_TOPIC)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--interval-seconds", type=int, default=int(os.environ.get("REALTIME_INTERVAL_SECONDS", "60")))
    parser.add_argument("--max-records", type=int, default=int(os.environ.get("REALTIME_MAX_RECORDS", "0")))
    parser.add_argument("--loop", action="store_true")
    args = parser.parse_args()

    producer = KafkaProducer(
        bootstrap_servers=args.bootstrap_servers,
        value_serializer=lambda value: json.dumps(value, separators=(",", ":")).encode("utf-8"),
        linger_ms=100,
        retries=5,
    )

    try:
        while True:
            publish_once(producer, args.topic, args.url, args.max_records)
            if not args.loop:
                break
            time.sleep(args.interval_seconds)
    finally:
        producer.close()


if __name__ == "__main__":
    main()
