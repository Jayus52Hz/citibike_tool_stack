# Citi Bike Realtime Kafka Log

Run ID: 20260610_204031
Run time: 2026-06-10 20:40:58

## Kafka

- Topic: `citibike.station_status`
- Published station status messages: 200
- Consumer group: `citibike-realtime-validation-20260610_204031`

## MySQL

- Table: `citibike_station_status_stream`
- Rows loaded from Kafka: 200

## Realtime Flow

GBFS station_status JSON -> `realtime/producer.py` -> Kafka topic `citibike.station_status` -> `realtime/consumer_mysql.py` -> MySQL table `citibike_station_status_stream`.

## Topic Description

```text
Topic: citibike.station_status	TopicId: 5gT9PG5TQK6H6-v7pFm22Q	PartitionCount: 1	ReplicationFactor: 1	Configs:
	Topic: citibike.station_status	Partition: 0	Leader: 1	Replicas: 1	Isr: 1

```

## MySQL Sample

```text
station_id	observed_at	num_bikes_available	num_docks_available	kafka_topic	kafka_offset
2124037250266884686	2026-06-10 13:40:50	10	0	citibike.station_status	0
ed279ef2-52ee-4ff2-9a52-edd8137ea034	2026-06-10 13:40:50	11	15	citibike.station_status	1
d18512f9-52c8-4175-92b9-b6258dc30748	2026-06-10 13:40:50	10	10	citibike.station_status	2
44fa161f-eb62-459b-b53e-da83788cfa2a	2026-06-10 13:40:50	8	20	citibike.station_status	3
1862008939006380034	2026-06-10 13:40:50	7	9	citibike.station_status	4
66db9c2e-0aca-11e7-82f6-3863bb44ef7c	2026-06-10 13:40:50	12	27	citibike.station_status	5
66de0a78-0aca-11e7-82f6-3863bb44ef7c	2026-06-10 13:40:50	12	5	citibike.station_status	6
66dbe571-0aca-11e7-82f6-3863bb44ef7c	2026-06-10 13:40:50	0	53	citibike.station_status	7
26cae473-0e59-4af7-bad5-bb6fec85c8bc	2026-06-10 13:40:50	0	21	citibike.station_status	8
2171903608969565866	2026-06-10 13:40:50	1	17	citibike.station_status	9

```

## Full Command Transcript

See: `D:\Bigdata\New game\citibike_tool_stack\logs\citibike_realtime_20260610_204031.log`
