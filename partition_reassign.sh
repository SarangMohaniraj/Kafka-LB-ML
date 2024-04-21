#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <topic_name> <broker_list> <bootstrap_server>"
    exit 1
fi

topic_name=$1
broker_list=$2
bootstrap_server=$3

echo '{
  "topics": [
    {"topic": "'$topic_name'"}
  ],
  "version": 1
}' > change_topics.json

output=$(/bin/kafka-reassign-partitions --bootstrap-server $bootstrap_server \
                                        --topics-to-move-json-file change_topics.json \
                                        --broker-list "$broker_list" \
                                        --generate)

proposed_json=$(echo "$output" | sed -n '/Proposed partition reassignment configuration/{:a;n;/^}/!ba;p}')

echo "$proposed_json" > reassignment.json

execution_output=$(/bin/kafka-reassign-partitions --bootstrap-server $bootstrap_server \
                                                  --reassignment-json-file reassignment.json \
                                                  --execute)

if echo "$execution_output" | grep -q "Success"; then
    echo "Partition reassignment executed successfully."
    rm change_topics.json reassignment.json
else
    echo "Partition reassignment execution failed."
    exit 1
fi
