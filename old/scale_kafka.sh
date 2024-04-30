#!/bin/bash

# The base port numbers for external and internal listeners.
base_external_port=29092
base_internal_port=19092
base_jmx_port=9999

# The number of Kafka instances you want to run.
num_instances=$1

if [ -z "$num_instances" ]; then
  echo "Usage: $0 <number_of_instances>"
  exit 1
fi

for ((i=1; i<=num_instances; i++)); do
  # Calculate the port numbers for this instance.
  external_port=$((base_external_port + i))
  internal_port=$((base_internal_port + i))
  jmx_port=$((base_jmx_port + i))

  # Use `docker run` to start a new Kafka instance with dynamically assigned ports and a unique broker ID.
  docker run -d \
    --name kafka$i \
    -e KAFKA_BROKER_ID=$i \
    -e KAFKA_ZOOKEEPER_CONNECT=zoo1:2181 \
    -e KAFKA_ADVERTISED_LISTENERS=EXTERNAL://localhost:$external_port,INTERNAL://kafka$i:$internal_port \
    -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=EXTERNAL:PLAINTEXT,INTERNAL:PLAINTEXT \
    -e KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL \
    -p $external_port:$external_port \
    -p $internal_port:$internal_port \
    -p $jmx_port:$jmx_port \
    confluentinc/cp-kafka:7.3.2
done
