ARG BASE_IMAGE=bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8
FROM ${BASE_IMAGE}

USER root

RUN set -eux; \
    printf '%s\n' \
      'deb [trusted=yes] http://snapshot.debian.org/archive/debian/20200130T000000Z stretch main' \
      'deb [trusted=yes] http://snapshot.debian.org/archive/debian-security/20200130T000000Z stretch/updates main' \
      'deb [trusted=yes] http://snapshot.debian.org/archive/debian/20200130T000000Z stretch-updates main' \
      > /etc/apt/sources.list; \
    apt-get -o Acquire::Check-Valid-Until=false update; \
    apt-get install -y --allow-unauthenticated --no-install-recommends python3-minimal; \
    ln -sf /usr/bin/python3 /usr/local/bin/python; \
    rm -rf /var/lib/apt/lists/*
