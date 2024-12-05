FROM postgres:16

# Install the necessary dependencies for building TimescaleDB from source and pgvector
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    postgresql-server-dev-16 \
    wget \
    git \
    cmake \
    ca-certificates \
    cron \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install TimescaleDB 2.17.2 and build it from source
RUN wget https://github.com/timescale/timescaledb/archive/refs/tags/2.17.2.tar.gz \
    && tar -xvf 2.17.2.tar.gz \
    && cd timescaledb-2.17.2 \
    && ./bootstrap \
    && cd build && make && make install \
    && cd ../.. \
    && rm -rf timescaledb-2.17.2 2.17.2.tar.gz

# Install pgvector and build it from source
RUN git clone https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make && make install \
    && cd .. \
    && rm -rf pgvector

# Setup the data directory and permissions
RUN mkdir -p /var/lib/postgresql/data && chown -R postgres:postgres /var/lib/postgresql/data
VOLUME /var/lib/postgresql/data

# Add PostgreSQL custom configurations
RUN echo "listen_addresses = '*'" >> /usr/share/postgresql/postgresql.conf.sample \
    && echo "shared_preload_libraries = 'timescaledb'" >> /usr/share/postgresql/postgresql.conf.sample

# Create a virtual environment and install Python dependencies inside it
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install psycopg2-binary fastapi uvicorn pandas python-dotenv pytest

# Set the enviroment variable for the PostgreSQL data directory
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=KPI_database
ENV POSTGRES_HOST_AUTH_METHOD=md5
# Expose PostgreSQL and FastAPI ports
EXPOSE 5432
EXPOSE 8002

# Copy the application directory into the container
COPY ./app /app
COPY ./exports.sql /docker-entrypoint-initdb.d/exports.sql

# Change ownership of the app directory to avoid permission issues
RUN chown -R postgres:postgres /app

# Run PostgreSQL as the default user and start FastAPI app
USER postgres

CMD ["/bin/bash", "-c", "docker-entrypoint.sh postgres & sleep 10 && /opt/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8002"]