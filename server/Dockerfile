# Stage 1: Build PostgreSQL from source
FROM alpine:3.20 AS postgresql_builder

# Install necessary dependencies
RUN set -eux; \
    addgroup -g 70 -S postgres; \
    adduser -u 70 -S -D -G postgres -H -h /var/lib/postgresql -s /bin/sh postgres; \
    mkdir -p /var/lib/postgresql; \
    chown -R postgres:postgres /var/lib/postgresql

# grab gosu for easy step-down from root
ENV GOSU_VERSION 1.17
RUN set -eux; \
    apk add --no-cache --virtual .gosu-deps \
        ca-certificates \
        dpkg \
        gnupg \
        wget \
    ; \
    dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
    wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
    wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
    export GNUPGHOME="$(mktemp -d)"; \
    gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
    gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
    gpgconf --kill all; \
    rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc; \
    apk del --no-network .gosu-deps; \
    chmod +x /usr/local/bin/gosu; \
    gosu --version; \
    gosu nobody true

RUN set -eux; ln -svf gosu /usr/local/bin/su-exec; su-exec nobody true

# make the "en_US.UTF-8" locale so postgres will be utf-8 enabled by default
ENV LANG en_US.utf8

RUN mkdir /docker-entrypoint-initdb.d

ENV PG_MAJOR 16
ENV PG_VERSION 16.3
ENV PG_SHA256 331963d5d3dc4caf4216a049fa40b66d6bcb8c730615859411b9518764e60585

ENV DOCKER_PG_LLVM_DEPS \
        llvm15-dev \
        clang15

RUN set -eux; \
    wget -O postgresql.tar.bz2 "https://ftp.postgresql.org/pub/source/v$PG_VERSION/postgresql-$PG_VERSION.tar.bz2"; \
    echo "$PG_SHA256 *postgresql.tar.bz2" | sha256sum -c -; \
    mkdir -p /usr/src/postgresql; \
    tar --extract --file postgresql.tar.bz2 --directory /usr/src/postgresql --strip-components 1; \
    rm postgresql.tar.bz2; \
    apk add --no-cache --virtual .build-deps \
        $DOCKER_PG_LLVM_DEPS \
        bison \
        coreutils \
        dpkg-dev dpkg \
        flex \
        g++ \
        gcc \
        krb5-dev \
        libc-dev \
        libedit-dev \
        libxml2-dev \
        libxslt-dev \
        linux-headers \
        make \
        openldap-dev \
        openssl-dev \
        perl-dev \
        perl-ipc-run \
        perl-utils \
        python3-dev \
        tcl-dev \
        util-linux-dev \
        zlib-dev \
        icu-dev \
        lz4-dev \
        zstd-dev \
    ; \
    cd /usr/src/postgresql; \
    awk '$1 == "#define" && $2 == "DEFAULT_PGSOCKET_DIR" && $3 == "\"/tmp\"" { $3 = "\"/var/run/postgresql\""; print; next } { print }' src/include/pg_config_manual.h > src/include/pg_config_manual.h.new; \
    grep '/var/run/postgresql' src/include/pg_config_manual.h.new; \
    mv src/include/pg_config_manual.h.new src/include/pg_config_manual.h; \
    gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"; \
    wget -O config/config.guess 'https://git.savannah.gnu.org/cgit/config.git/plain/config.guess?id=7d3d27baf8107b630586c962c057e22149653deb'; \
    wget -O config/config.sub 'https://git.savannah.gnu.org/cgit/config.git/plain/config.sub?id=7d3d27baf8107b630586c962c057e22149653deb'; \
    export LLVM_CONFIG="/usr/lib/llvm15/bin/llvm-config"; \
    export CLANG=clang-15; \
    ./configure \
        --enable-option-checking=fatal \
        --build="$gnuArch" \
        --enable-integer-datetimes \
        --enable-thread-safety \
        --enable-tap-tests \
        --disable-rpath \
        --with-uuid=e2fs \
        --with-pgport=5432 \
        --with-system-tzdata=/usr/share/zoneinfo \
        --prefix=/usr/local \
        --with-includes=/usr/local/include \
        --with-libraries=/usr/local/lib \
        --with-gssapi \
        --with-ldap \
        --with-tcl \
        --with-perl \
        --with-python \
        --with-openssl \
        --with-libxml \
        --with-libxslt \
        --with-icu \
        --with-llvm \
        --with-lz4 \
        --with-zstd \
    ; \
    make -j "$(nproc)" world-bin; \
    make install-world-bin; \
    make -C contrib install; \
    runDeps="$( \
        scanelf --needed --nobanner --format '%n#p' --recursive /usr/local \
            | tr ',' '\n' \
            | sort -u \
            | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
            | grep -v -e perl -e python -e tcl \
    )"; \
    apk add --no-cache --virtual .postgresql-rundeps \
        $runDeps \
        bash \
        tzdata \
        zstd \
        icu-data-full \
        $([ "$(apk --print-arch)" != 'ppc64le' ] && echo 'nss_wrapper') \
    ; \
    apk del --no-network .build-deps; \
    cd /; \
    rm -rf /usr/src/postgresql /usr/local/share/doc /usr/local/share/man; \
    postgres --version

# make the sample config easier to munge (and "correct by default")
RUN set -eux; \
    cp -v /usr/local/share/postgresql/postgresql.conf.sample /usr/local/share/postgresql/postgresql.conf.sample.orig; \
    sed -ri "s!^#?(listen_addresses)\s*=\s*\S+.*!\1 = '*'!" /usr/local/share/postgresql/postgresql.conf.sample; \
    grep -F "listen_addresses = '*'" /usr/local/share/postgresql/postgresql.conf.sample

RUN mkdir -p /var/run/postgresql && chown -R postgres:postgres /var/run/postgresql && chmod 3777 /var/run/postgresql

ENV PGDATA /var/lib/postgresql/data
RUN mkdir -p "$PGDATA" && chown -R postgres:postgres "$PGDATA" && chmod 1777 "$PGDATA"
VOLUME /var/lib/postgresql/data

COPY init-db.sh /docker-entrypoint-initdb.d/

ENTRYPOINT ["postgres"]
STOPSIGNAL SIGINT
EXPOSE 5432


# Stage 2: Set up FastAPI with PostgreSQL
FROM python:3.9-alpine AS server_builder

ENV TZ=America/Santiago
ENV SECRET_KEY=48619d05440fae6b440c4416bd51cb82d236bb1bb4337cced967ed5a6d9ad388
ENV TIME_ALLOWED_MODIFICATION=72
ENV TIME_ALLOWED=24

ENV STATIC_DIRECTORY=/fastapi/server/storage/static/
ENV STATIC_DIRECTORY_URL=/api/static/

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=WxJHehShZN
ENV POSTGRES_DB=app.storage

ENV DATABASE_URL=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@172.40.40.122:5432/$POSTGRES_DB

LABEL maintainer="BACKEND"

WORKDIR /fastapi/server

COPY --from=postgresql_builder /usr/local /usr/local
COPY --from=postgresql_builder /var/lib/postgresql /var/lib/postgresql

COPY ./application/requirements.txt /fastapi/server/requirements.txt
RUN apk add --no-cache \
        postgresql-dev \
        gcc \
        musl-dev \
        python3-dev \
        libffi-dev \
        openssl-dev \
        libldap \
    && pip install --no-cache-dir --upgrade -r /fastapi/server/requirements.txt \
    && rm -rf /var/cache/apk/*

COPY ./application /fastapi/server/application

WORKDIR /fastapi/server/application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

