set -e

hdfs dfs -rm -r -f /sqoop/import/test_data || true

sqoop import \
  --connect "jdbc:mysql://mysql:3306/testdb?allowPublicKeyRetrieval=true&useSSL=false" \
  --username testuser \
  --password testpass \
  --driver com.mysql.cj.jdbc.Driver \
  --table test_data \
  --target-dir /sqoop/import/test_data \
  --delete-target-dir \
  --num-mappers 1 \
  --fields-terminated-by ","

hdfs dfs -cat /sqoop/import/test_data/part-m-00000

sqoop export \
  --connect "jdbc:mysql://mysql:3306/testdb?allowPublicKeyRetrieval=true&useSSL=false" \
  --username testuser \
  --password testpass \
  --driver com.mysql.cj.jdbc.Driver \
  --table sqoop_export_test \
  --export-dir /sqoop/import/test_data
