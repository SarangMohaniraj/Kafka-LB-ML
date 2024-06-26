import jpype
from jpype import JClass, JString

jpype.startJVM()


def get_kafka_metrics():
    metrics = {}
    JMXServiceURL = JClass("javax.management.remote.JMXServiceURL")
    JMXConnectorFactory = JClass("javax.management.remote.JMXConnectorFactory")
    HashMap = JClass("java.util.HashMap")
    url = JMXServiceURL("service:jmx:rmi:///jndi/rmi://localhost:9999/jmxrmi")
    jmxConnector = JMXConnectorFactory.connect(url, HashMap())
    mbsc = jmxConnector.getMBeanServerConnection()
    ObjectName = JClass("javax.management.ObjectName")

    # print("names", dir(mbsc))
    # nameSet = mbsc.queryMBeans(None, None)
    # print("names", nameSet)
    memory = "java.lang:type=Memory"
    mbeans = [
        memory,
        "java.lang:type=OperatingSystem",
        "kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec",
        "kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec",
        "kafka.server:type=ReplicaManager,name=PartitionCount",
        "kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce",
        "kafka.network:type=RequestMetrics,name=TotalTimeMs,request=FetchConsumer",
        "kafka.network:type=RequestMetrics,name=TotalTimeMs,request=FetchFollower",
        "kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec",
        "kafka.server:type=BrokerTopicMetrics,name=TotalProduceRequestsPerSec",
        # f"kafka.log:type=Log,name=Size,topic={topic_name},partition=7",
        # f"kafka.log:type=Log,name=NumLogSegments,topic={topic_name},partition=1",
        "kafka.server:type=Request",
        # "kafka.server:type=raft-metrics,name=poll-idle-ratio-avg",
        # f"kafka.server:type=BrokerTopicMetrics,name=RemoteLogSizeBytes,topic={topic_name}",
    ]

    for mbean in mbeans:
        print("=================================")
        metrics[str(mbean)] = {}
        print(mbean)
        info = mbsc.getMBeanInfo(ObjectName(mbean))
        for a in info.getAttributes():

            if a.getName() == "HeapMemoryUsage" or a.getName() == "NonHeapMemoryUsage":
                used_value = mbsc.getAttribute(
                    ObjectName(mbean), JString(a.getName())
                ).get("used")
                max_value = mbsc.getAttribute(
                    ObjectName(mbean), JString(a.getName())
                ).get("max")
                print("name", a.getName(), "used", used_value)
                print(
                    "name",
                    a.getName(),
                    "max",
                    max_value,
                )

                metrics[mbean][JString(a.getName())] = {
                    "used": str(used_value),
                    "max": str(max_value),
                }

            else:
                value = mbsc.getAttribute(ObjectName(mbean), str(JString(a.getName())))
                print(
                    "name",
                    a.getName(),
                    value,
                )
                metrics[str(mbean)][JString(a.getName())] = value
        print("=================================")
    jmxConnector.close()
    # Shutdown JVM
    # Shutdown JVM
    # jpype.shutdownJVM()
    return metrics
