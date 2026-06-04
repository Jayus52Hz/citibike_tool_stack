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

RUN set -eux; \
    curl --retry 5 --retry-delay 5 -fsSL "https://archive.apache.org/dist/sqoop/${SQOOP_VERSION}/sqoop-${SQOOP_VERSION}.bin__hadoop-2.6.0.tar.gz" -o /tmp/sqoop.tgz; \
    tar -xzf /tmp/sqoop.tgz -C /opt; \
    mv "/opt/sqoop-${SQOOP_VERSION}.bin__hadoop-2.6.0" "${SQOOP_HOME}"; \
    rm /tmp/sqoop.tgz; \
    curl --retry 5 --retry-delay 5 -fsSL "https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/${MYSQL_CONNECTOR_VERSION}/mysql-connector-j-${MYSQL_CONNECTOR_VERSION}.jar" -o "${SQOOP_HOME}/lib/mysql-connector-j.jar"; \
    curl --retry 5 --retry-delay 5 -fsSL "https://repo1.maven.org/maven2/commons-lang/commons-lang/2.6/commons-lang-2.6.jar" -o "${SQOOP_HOME}/lib/commons-lang-2.6.jar"; \
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
