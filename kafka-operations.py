from confluent_kafka.admin import AdminClient, NewTopic
from cluster_props_handler import get_cluster_properties

def create_topic(topic_name, num_partitions=3, rf=2):
    cluster_properties = get_cluster_properties()
    bootstrap_servers = ",".join(cluster_properties["brokers_servers"])
    a = AdminClient({'bootstrap.servers': bootstrap_servers})
    new_topics = [NewTopic(topic, num_partitions=num_partitions, replication_factor=rf) for topic in [topic_name]]
    fs = a.create_topics(new_topics)
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))

if __name__ == "__main__":
    create_topic("topic2",2,2)