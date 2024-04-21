from confluent_kafka.admin import AdminClient, NewTopic
from cluster_props_handler import get_cluster_properties

def create_topic(topic_name):
    cluster_properties = get_cluster_properties()
    bootstrap_servers = ",".join(cluster_properties["brokers_servers"])
    a = AdminClient({'bootstrap.servers': bootstrap_servers})
    new_topics = [NewTopic(topic, num_partitions=3, replication_factor=2) for topic in [topic_name]]
    fs = a.create_topics(new_topics)
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))
    
create_topic("example_topic-5")