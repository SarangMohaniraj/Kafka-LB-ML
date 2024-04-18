from kafka.admin import KafkaAdminClient, NewTopic, ConfigResource, ConfigResourceType
from kafka.client_async import KafkaClient
from kafka.cluster import ClusterMetadata
from kafka import KafkaProducer
from pprint import pprint
from kafka.admin.new_partitions import NewPartitions
import json as json

def serializer(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)
print("producer", producer.config['client_id'])
print("----------Producer Info---------")
print("producer", producer.config)
print("----------Producer Info---------")
# producer_client_id = 'my_producer_client'
# producer = KafkaProducer(client_id=producer_client_id)

# producer.send()


# from kafka.protocol.admin import ListTopicsRequest

# Initialize KafkaAdminClient with bootstrap server(s)
bootstrap_servers = "localhost:9092"  # Change this to your Kafka bootstrap server(s)
admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
cluster_metadata = ClusterMetadata(bootstrap_servers=bootstrap_servers)
cl = admin_client._get_cluster_metadata()
print("cl", cl, type(cl))
print("desc clusters", admin_client.describe_cluster())
print("desc topics", admin_client.describe_topics())
print("metrics", admin_client._metrics.metric_name.__name__)

resources = [ConfigResource(ConfigResourceType.TOPIC, 1)]

print("====================")
pprint(admin_client.describe_configs(resources))

print("====================")

# admin_client.create_partitions({
#     "example_topic": NewPartitions(8)
# })

# Fetch metadata about topics
topics = admin_client.describe_topics()
print("List of topics:")
for topic in topics:
    print(topic)

# Alternatively, you can use KafkaClient to get metadata
kafka_client = KafkaClient(bootstrap_servers=bootstrap_servers)
cluster_metadata = kafka_client.cluster
print("cluster metadat", cluster_metadata)
print("\nMetadata about brokers:")
print("Brokers:", cl.brokers)
print("\nMetadata about topics and partitions:")
print("Topics:", cl.topics)

# BrokerMetadata
partition_distribution = {}
for topic in topics:
    print(topic.keys())
    top = topic["topic"]
    partitions = topic["partitions"]
    print("top", top)
    print("partitions", partitions)
    print("cluster_metadata available_partitions_for_topic")
    for partition in partitions:
        print("partition", partition)
        # Get leader broker for each partition
#         leader_broker = cluster_metadata.leader_for_partition(partition)
#         if leader_broker:
#             # Add leader broker to partition distribution
#             partition_distribution.setdefault(leader_broker.nodeId, []).append((topic, partition))
# # return partition_distribution


import jpype
from jpype import JClass, JString

# Start JVM
jpype.startJVM()
# Create JMX connection
JMXServiceURL = JClass("javax.management.remote.JMXServiceURL")
JMXConnectorFactory = JClass("javax.management.remote.JMXConnectorFactory")
HashMap = JClass("java.util.HashMap")
url = JMXServiceURL("service:jmx:rmi:///jndi/rmi://localhost:9999/jmxrmi")
jmxConnector = JMXConnectorFactory.connect(url, HashMap())
mbsc = jmxConnector.getMBeanServerConnection()
# Define Kafka broker's MBean name
# Get memory and CPU usage metrics
ObjectName = JClass("javax.management.ObjectName")

print("names", dir(mbsc))
nameSet = mbsc.queryMBeans(None, None)
print("names", nameSet)
memory = "java.lang:type=Memory"
mbeans = [
    memory,
    "java.lang:type=OperatingSystem",
    "kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec",
    "kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec",
    # "kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec,topic=",
    "kafka.server:type=ReplicaManager,name=PartitionCount",
    "kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce",
    "kafka.network:type=RequestMetrics,name=TotalTimeMs,request=FetchConsumer",
    "kafka.network:type=RequestMetrics,name=TotalTimeMs,request=FetchFollower",
    "kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec",
    "kafka.server:type=BrokerTopicMetrics,name=TotalProduceRequestsPerSec",
    "kafka.log:type=Log,name=Size,topic=example_topic,partition=7",
    "kafka.log:type=Log,name=NumLogSegments,topic=example_topic,partition=1",
    # "kafka.consumer:type=consumer-fetch-manager-metrics,client-id="+producer.config['client_id']
    "kafka.server:type=Request",
    "kafka.server:type=raft-metrics,name=poll-idle-ratio-avg",
    "kafka.server:type=BrokerTopicMetrics,name=RemoteLogSizeBytes,topic=example_topic"
    # "kafka.producer:type=producer-metrics,client-id="+producer.config['client_id']+',name=RequestLatencyAvg'
    ]



for mbean in mbeans:
    print("=================================")
    print(mbean)
    info = mbsc.getMBeanInfo(ObjectName(mbean))
    for a in info.getAttributes():

        if a.getName() == "HeapMemoryUsage" or a.getName() == "NonHeapMemoryUsage":
            print(
                "name",
                a.getName(),
                "used",
                mbsc.getAttribute(ObjectName(mbean), JString(a.getName())).get("used"),
            )
            print(
                "name",
                a.getName(),
                "max",
                mbsc.getAttribute(ObjectName(mbean), JString(a.getName())).get("max"),
            )

        else:
            print(
                "name",
                a.getName(),
                mbsc.getAttribute(ObjectName(mbean), JString(a.getName())),
            )
    print("=================================")
jmxConnector.close()
# Shutdown JVM
jpype.shutdownJVM()
