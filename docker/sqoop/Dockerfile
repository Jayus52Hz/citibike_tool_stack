FROM eclipse-temurin:8-jdk-jammy

ARG HADOOP_VERSION=3.3.6
ARG SQOOP_VERSION=1.4.7
ARG MYSQL_CONNECTOR_VERSION=8.0.33

ENV HADOOP_HOME=/opt/hadoop \
    HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop \
    HADOOP_COMMON_HOME=/opt/hadoop \
    HADOOP_HDFS_HOME=/opt/hadoop \
    HADOOP_MAPRED_HOME=/opt/hadoop \
    HADOOP_YARN_HOME=/opt/hadoop \
    SQOOP_HOME=/opt/sqoop \
    PATH=/opt/sqoop/bin:/opt/hadoop/bin:/opt/hadoop/sbin:$PATH

RUN set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      bash \
      ca-certificates \
      curl \
      default-mysql-client \
      gzip \
      netcat-openbsd \
      procps \
      tar; \
    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    curl -fsSL "https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" -o /tmp/hadoop.tgz; \
    tar -xzf /tmp/hadoop.tgz -C /opt; \
    mv "/opt/hadoop-${HADOOP_VERSION}" "${HADOOP_HOME}"; \
    rm /tmp/hadoop.tgz

RUN set -eux; \
    curl -fsSL "https://archive.apache.org/dist/sqoop/${SQOOP_VERSION}/sqoop-${SQOOP_VERSION}.bin__hadoop-2.6.0.tar.gz" -o /tmp/sqoop.tgz; \
    tar -xzf /tmp/sqoop.tgz -C /opt; \
    mv "/opt/sqoop-${SQOOP_VERSION}.bin__hadoop-2.6.0" "${SQOOP_HOME}"; \
    rm /tmp/sqoop.tgz; \
    curl -fsSL "https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/${MYSQL_CONNECTOR_VERSION}/mysql-connector-j-${MYSQL_CONNECTOR_VERSION}.jar" -o "${SQOOP_HOME}/lib/mysql-connector-j.jar"; \
    curl -fsSL "https://repo1.maven.org/maven2/commons-lang/commons-lang/2.6/commons-lang-2.6.jar" -o "${SQOOP_HOME}/lib/commons-lang-2.6.jar"; \
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
