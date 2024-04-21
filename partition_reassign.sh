#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <topic_name_list> <broker_list> <bootstrap_server>"
    exit 1
fi

topic_names=$1
broker_list=$2
bootstrap_server=$3

IFS=',' read -ra topics <<< "$topic_names"

echo '{
  "topics": [' > change_topics.json

for topic in "${topics[@]}"; do
    echo '    {"topic": "'"$topic"'"},' >> change_topics.json
done

echo '  ],
  "version": 1
}' >> change_topics.json

# Remove trailing comma
sed -i '$s/,$//' change_topics.json

output=$(/bin/kafka-reassign-partitions --bootstrap-server $bootstrap_server \
                                        --topics-to-move-json-file change_topics.json \
                                        --broker-list "$broker_list" \
                                        --generate)

proposed_json=$(echo "$output" | awk '/Proposed partition reassignment configuration/{flag=1; next} /Current partition replica assignment/{flag=0} flag')

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
