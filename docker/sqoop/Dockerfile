FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

ARG SQOOP_VERSION=1.4.7
ARG MYSQL_CONNECTOR_VERSION=8.0.33

ENV HADOOP_HOME=/opt/hadoop-3.2.1 \
    HADOOP_CONF_DIR=/opt/hadoop-3.2.1/etc/hadoop \
    HADOOP_COMMON_HOME=/opt/hadoop-3.2.1 \
    HADOOP_HDFS_HOME=/opt/hadoop-3.2.1 \
    HADOOP_MAPRED_HOME=/opt/hadoop-3.2.1 \
    HADOOP_YARN_HOME=/opt/hadoop-3.2.1 \
    SQOOP_HOME=/opt/sqoop \
    PATH=/opt/sqoop/bin:/opt/hadoop-3.2.1/bin:/opt/hadoop-3.2.1/sbin:$PATH

# Copy từ local thay vì curl
COPY deps/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz /tmp/sqoop.tgz
COPY deps/mysql-connector-j-8.0.33.jar /tmp/mysql-connector-j.jar
COPY deps/commons-lang-2.6.jar /tmp/commons-lang-2.6.jar

RUN set -eux; \
    tar -xzf /tmp/sqoop.tgz -C /opt; \
    mv "/opt/sqoop-${SQOOP_VERSION}.bin__hadoop-2.6.0" "${SQOOP_HOME}"; \
    rm /tmp/sqoop.tgz; \
    mv /tmp/mysql-connector-j.jar "${SQOOP_HOME}/lib/mysql-connector-j.jar"; \
    mv /tmp/commons-lang-2.6.jar "${SQOOP_HOME}/lib/commons-lang-2.6.jar"; \
    cp "${SQOOP_HOME}/conf/sqoop-env-template.sh" "${SQOOP_HOME}/conf/sqoop-env.sh"; \
    { \
      echo "export HADOOP_COMMON_HOME=${HADOOP_HOME}"; \
      echo "export HADOOP_HDFS_HOME=${HADOOP_HOME}"; \
      echo "export HADOOP_MAPRED_HOME=${HADOOP_HOME}"; \
      echo "export HADOOP_YARN_HOME=${HADOOP_HOME}"; \
      echo "export HADOOP_CONF_DIR=${HADOOP_CONF_DIR}"; \
    } >> "${SQOOP_HOME}/conf/sqoop-env.sh"

WORKDIR /workspace
CMD ["bash", "-lc", "tail -f /dev/null"]