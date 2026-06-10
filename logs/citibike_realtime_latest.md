# Citi Bike Realtime Kafka Log

Run ID: 20260610_095935
Run time: 2026-06-10 10:00:16

## Kafka

- Topic: `citibike.station_status`
- Published station status messages: 200
- Consumer group: `citibike-realtime-validation-20260610_095935`

## MySQL

- Table: `citibike_station_status_stream`
- Rows loaded from Kafka: 200

## Realtime Flow

GBFS station_status JSON -> `realtime/producer.py` -> Kafka topic `citibike.station_status` -> `realtime/consumer_mysql.py` -> MySQL table `citibike_station_status_stream`.

## Topic Description

```text
Topic: citibike.station_status	TopicId: WUfOLjJqTOmAB2NLER6K8w	PartitionCount: 1	ReplicationFactor: 1	Configs: 
	Topic: citibike.station_status	Partition: 0	Leader: 1	Replicas: 1	Isr: 1

```

## MySQL Sample

```text
station_id	observed_at	num_bikes_available	num_docks_available	kafka_topic	kafka_offset
2206772051528680770	2026-06-10 03:00:15	0	0	citibike.station_status	0
2206771530409556572	2026-06-10 03:00:15	0	0	citibike.station_status	1
af72ab76-c6cb-4994-af96-51fa8846ecdc	2026-06-10 03:00:15	0	0	citibike.station_status	2
2206778196198800034	2026-06-10 03:00:15	0	0	citibike.station_status	3
06439006-11b6-44f0-8545-c9d39035f32a	2026-06-10 03:00:15	0	0	citibike.station_status	4
2206780889143294664	2026-06-10 03:00:15	0	0	citibike.station_status	5
2206781040135081610	2026-06-10 03:00:15	0	0	citibike.station_status	6
2206782424530885178	2026-06-10 03:00:15	0	0	citibike.station_status	7
2206779090602992084	2026-06-10 03:00:15	0	0	citibike.station_status	8
2206779404135604698	2026-06-10 03:00:15	0	0	citibike.station_status	9

```

## Full Command Transcript

See: `D:\Bigdata\citibike_tool_stack\logs\citibike_realtime_20260610_095935.log`
