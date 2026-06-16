# Citi Bike Realtime Kafka Log

Run ID: 20260612_200349
Run time: 2026-06-12 20:04:13

## Kafka

- Topic: `citibike.station_status`
- Published station status messages: 200
- Consumer group: `citibike-realtime-validation-20260612_200349`

## MySQL

- Table: `citibike_station_status_stream`
- Rows loaded from Kafka: 200

## Realtime Flow

GBFS station_status JSON -> `realtime/producer.py` -> Kafka topic `citibike.station_status` -> `realtime/consumer_mysql.py` -> MySQL table `citibike_station_status_stream`.

## Topic Description

```text
Topic: citibike.station_status	TopicId: 9P-KtDn3RSuQRwF-dgdvhA	PartitionCount: 1	ReplicationFactor: 1	Configs: 
	Topic: citibike.station_status	Partition: 0	Leader: 1	Replicas: 1	Isr: 1

```

## MySQL Sample

```text
station_id	observed_at	num_bikes_available	num_docks_available	kafka_topic	kafka_offset
7dda8844-60ba-4449-b05c-54c1d14ab5fb	2026-06-12 13:04:03	0	0	citibike.station_status	0
af72ab76-c6cb-4994-af96-51fa8846ecdc	2026-06-12 13:04:03	0	0	citibike.station_status	1
2206778196198800034	2026-06-12 13:04:03	0	0	citibike.station_status	2
06439006-11b6-44f0-8545-c9d39035f32a	2026-06-12 13:04:03	0	0	citibike.station_status	3
2206780889143294664	2026-06-12 13:04:03	0	0	citibike.station_status	4
2206781040135081610	2026-06-12 13:04:03	0	0	citibike.station_status	5
2206782424530885178	2026-06-12 13:04:03	0	0	citibike.station_status	6
2206779090602992084	2026-06-12 13:04:03	0	0	citibike.station_status	7
2206779404135604698	2026-06-12 13:04:03	0	0	citibike.station_status	8
66dc292c-0aca-11e7-82f6-3863bb44ef7c	2026-06-12 13:04:03	0	0	citibike.station_status	9

```

## Full Command Transcript

See: `D:\Bigdata\New game\projects\citibike_tool_stack\logs\citibike_realtime_20260612_200349.log`

