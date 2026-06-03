# Manual Steps

File nay ghi cac buoc thu cong neu muon chung minh service qua UI hoac neu test tu dong gap loi do service khoi dong cham.

## Superset: Connect MySQL Manually

1. Mo http://localhost:8089 va login `admin` / `admin`.
2. Vao `Settings` -> `Database Connections` -> `+ Database`.
3. Chon MySQL hoac nhap SQLAlchemy URI:

```text
mysql+pymysql://testuser:testpass@mysql:3306/testdb
```

4. Bam `Test Connection`.
5. Neu thanh cong, tao dataset tu table `test_data`.

## Drill: Query CSV in UI

1. Mo http://localhost:8047.
2. Vao tab `Query`.
3. Chay SQL:

```sql
SELECT columns[0] AS id, columns[1] AS name, columns[2] AS value
FROM dfs.`/sample-data/test.csv`
WHERE columns[0] <> 'id';
```

Drillbit dung ZooKeeper noi bo `zookeeper:2181`. Neu UI chua len, kiem tra:

```powershell
docker compose ps zookeeper drill
docker compose logs --tail 80 drill
```

## Drill: Optional HDFS Storage Plugin

Neu muon query HDFS truc tiep:

1. Mo http://localhost:8047/storage.
2. Copy storage plugin `dfs`, dat ten moi `hdfs`.
3. Doi `connection` thanh:

```json
"connection": "hdfs://namenode:9000/"
```

4. Enable plugin va query duong dan HDFS, vi du sau khi chay HDFS test:

```sql
SELECT columns[0], columns[1], columns[2]
FROM hdfs.`/data/test/test.csv`;
```

## Airflow: Run DAG in UI

1. Mo http://localhost:8082 va login `admin` / `admin`.
2. Tim DAG `tool_stack_health_check`.
3. Bat DAG neu dang paused.
4. Bam trigger va doi trang thai success.

CLI tuong duong:

```powershell
.\scripts\test-airflow.ps1
```

## Kafka: Manual CLI

```powershell
docker compose exec kafka bash
kafka-topics.sh --bootstrap-server kafka:9092 --create --if-not-exists --topic tool-stack-test
printf "hello-bigdata\n" | kafka-console-producer.sh --bootstrap-server kafka:9092 --topic tool-stack-test
kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic tool-stack-test --from-beginning --max-messages 1 --timeout-ms 10000
```

## Sqoop: Manual CLI

```powershell
docker compose exec sqoop bash
sqoop import --connect "jdbc:mysql://mysql:3306/testdb?allowPublicKeyRetrieval=true&useSSL=false" --username testuser --password testpass --driver com.mysql.cj.jdbc.Driver --table test_data --target-dir /sqoop/import/test_data --delete-target-dir --num-mappers 1 --fields-terminated-by ','
hdfs dfs -cat /sqoop/import/test_data/part-m-00000
```

## MinIO UI

1. Mo http://localhost:9003.
2. Login `minioadmin` / `minioadmin`.
3. Kiem tra bucket `test-bucket`.
4. Kiem tra object `test.csv`.
